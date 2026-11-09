import https from 'node:https';
import {lookup} from 'node:dns/promises';
import {BlockList, isIP} from 'node:net';
import {gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
import {load} from 'cheerio';
import robotsParser from 'robots-parser';
import {EMBEDDING_MODEL, EMBEDDING_DIMENSIONS} from '../src/inventory-store.mjs';

const USER_AGENT = 'SuperMarketersInventory/1.0';
const MAX_BYTES = 2_000_000;
const privateIPs4 = new BlockList();
const privateIPs6 = new BlockList();
for (const [network, bits] of [['0.0.0.0',8],['10.0.0.0',8],['100.64.0.0',10],['127.0.0.0',8],
  ['169.254.0.0',16],['172.16.0.0',12],['192.0.0.0',24],['192.0.2.0',24],['192.168.0.0',16],
  ['198.18.0.0',15],['198.51.100.0',24],['203.0.113.0',24],['224.0.0.0',4],['240.0.0.0',4]]) privateIPs4.addSubnet(network,bits,'ipv4');
for (const [network,bits] of [['::',96],['::ffff:0:0',96],['64:ff9b::',96],['100::',64],
  ['2001::',23],['2002::',16],['fc00::',7],['fe80::',10],['ff00::',8]]) privateIPs6.addSubnet(network,bits,'ipv6');
export const isPublicIP = address => isIP(address) !== 0 && !(isIP(address) === 4 ? privateIPs4 : privateIPs6).check(address, isIP(address) === 4 ? 'ipv4' : 'ipv6');

export function scopedURL(value, host, base=`https://${host}/`) {
  const url = new URL(value, base);
  if (url.protocol !== 'https:' || url.port || url.username || url.password ||
      ![host, 'www.' + host].includes(url.hostname.toLowerCase())) throw Error('URL is outside the selected domain.');
  url.hash = '';
  return url.href;
}

export async function publicRequest(value, host, redirects=0, allowed=()=>true) {
  const url = new URL(scopedURL(value, host));
  if(!allowed(url.href))throw Error('Blocked by robots.txt.');
  if (redirects > 5) throw Error('Too many redirects.');
  const addresses = await lookup(url.hostname, {all:true});
  if (!addresses.length || addresses.some(a => !isPublicIP(a.address))) throw Error('Domain does not resolve exclusively to public addresses.');
  const result = await new Promise((resolve,reject) => {
    const request = https.get(url, {signal:AbortSignal.timeout(30000),headers:{'User-Agent':USER_AGENT,'Accept-Encoding':'identity'},
      lookup: (_host,options,callback) => options.all ? callback(null,addresses) : callback(null,addresses[0].address,addresses[0].family)}, response => {
      if ([301,302,303,307,308].includes(response.statusCode)) {
        response.resume();
        try { if(!response.headers.location)throw Error('Redirect has no destination.');resolve({redirect:scopedURL(response.headers.location,host,url.href)}); } catch(e) { reject(e); }
        return;
      }
      const chunks=[]; let length=0;
      response.on('data',chunk=>{length+=chunk.length;if(length>MAX_BYTES) response.destroy(Error('Response exceeds the 2 MB limit.'));else chunks.push(chunk);});
      response.on('error',reject);
      response.on('end',()=>{try {
        let body=Buffer.concat(chunks);
        if (response.headers['content-encoding']==='gzip' || (body[0]===0x1f && body[1]===0x8b)) body=gunzipSync(body,{maxOutputLength:MAX_BYTES});
        resolve({status:response.statusCode,type:String(response.headers['content-type']||''),body:body.toString('utf8'),url:url.href});
      } catch { reject(Error('Unable to decode the response.')); }});
    });
    request.setTimeout(30000,()=>request.destroy(Error('Request timed out.')));
    request.on('error',()=>reject(Error('Website connection failed.')));
  });
  return result.redirect ? publicRequest(result.redirect,host,redirects+1,allowed) : result;
}

export function parsePage(response) {
  if (response.status !== 200) throw Error('Page returned HTTP ' + response.status + '.');
  if (!/text\/html|application\/xhtml\+xml/i.test(response.type)) throw Error('Page is not HTML.');
  const $=load(response.body);
  const title=$('title').first().text().trim();
  const description=$('meta[name="description"]').first().attr('content')||'';
  const canonical=$('link[rel="canonical"]').first().attr('href')||'';
  const robots=$('meta[name="robots"]').first().attr('content')||'';
  $('script,style,noscript,template,nav,footer,header').remove();
  const root=$('main').first().length ? $('main').first() : $('article').first().length ? $('article').first() : $('body');
  root.find('p,h1,h2,h3,h4,li,tr,br').prepend('\n');
  const content=root.text().split('\n').map(s=>s.replace(/\s+/g,' ').trim()).filter(Boolean).join('\n');
  if (!content) throw Error('No readable page content; JavaScript rendering is not included.');
  const hash=createHash('sha256').update(JSON.stringify({title,description,content})).digest('hex');
  return {url:response.url,title,description,content,canonical,robots,hash,status:response.status};
}

export function embeddingInput(page) {
  // Every UTF-8 byte is an upper bound of one token; remain below 8192 even for non-English pages.
  return Buffer.from(`${page.title}\n\n${page.content}`.trim()).subarray(0,8000).toString('utf8');
}

export async function embedPage(page, key) {
  if (!key) throw Error('OPENAI_API_KEY is required for indexing.');
  let response;
  try { response=await fetch('https://api.openai.com/v1/embeddings',{method:'POST',redirect:'error',
    signal:AbortSignal.timeout(60000),headers:{'Content-Type':'application/json',Authorization:'Bearer '+key},
    body:JSON.stringify({model:EMBEDDING_MODEL,dimensions:EMBEDDING_DIMENSIONS,input:embeddingInput(page),encoding_format:'float'})}); }
  catch { throw Error('Embedding connection failed; rerun to retry indexing.'); }
  if (!response.ok) throw Error('Embedding API returned HTTP '+response.status+'.');
  let result; try { result=await response.json(); } catch { throw Error('Invalid embedding response.'); }
  if (result.model !== EMBEDDING_MODEL || !Array.isArray(result.data) || result.data.length!==1 || result.data[0].index!==0) throw Error('Unexpected embedding response.');
  return result.data[0].embedding;
}

export async function refreshInventory(store, domainId, {request=publicRequest,embed,key,maxPages=200,signal}={}) {
  if (!Number.isInteger(maxPages)||maxPages<1||maxPages>1000) throw Error('maxPages must be between 1 and 1000.');
  const domain=store.domain(domainId); if (!domain) throw Error('Unknown domain.');
  const token=store.begin(domainId);
  let ownershipError;
  const timer=setInterval(()=>{try{store.heartbeat(domainId,token);}catch(error){ownershipError=error;}},15000);
  const deadline=Date.now()+600000;
  const available=()=>{if(ownershipError)throw ownershipError;if(signal?.aborted)throw Error('Refresh interrupted.');if(Date.now()>deadline)throw Error('Refresh reached its 10 minute time limit.');};
  const get=async (url,allowed)=>{available();return request(scopedURL(url,domain.host),domain.host,0,allowed);};
  const issues=[];let fetched=0,indexed=0;
  try {
    const origin=`https://${domain.host}`;
    const robots=await get(origin+'/robots.txt');
    if (robots.status!==200 && robots.status!==404) throw Error('Cannot establish robots policy: HTTP '+robots.status+'.');
    const policy=robotsParser(origin+'/robots.txt',robots.status===200?robots.body:'');
    const allowed=url=>{const check=new URL(url);check.hostname=domain.host;return policy.isAllowed(check.href,USER_AGENT)!==false;};
    const delay=policy.getCrawlDelay(USER_AGENT)||0;
    if (delay>0) throw Error('This site requests a crawl delay; paced crawling is not supported yet.');
    const maps=[...policy.getSitemaps(),origin+'/sitemap.xml',origin+'/sitemap_index.xml',origin+'/wp-sitemap.xml'];
    const requiredMaps=new Set(policy.getSitemaps());
    const seen=new Set(), urls=new Set();let found=false;
    while(maps.length && seen.size<20 && urls.size<maxPages) {
      const next=maps.shift();if(seen.has(next))continue;seen.add(next);
      try {
        const response=await get(next);
        if(response.status===404){if(requiredMaps.has(next))issues.push('A declared sitemap could not be fetched.');continue;}
        if(response.status!==200)throw Error('Sitemap returned HTTP '+response.status+'.');
        if(/<!DOCTYPE|<!ENTITY/i.test(response.body))throw Error('Unsafe sitemap XML.');
        const $=load(response.body,{xmlMode:true});
        const type=$.root().children().first().get(0)?.name?.split(':').at(-1);
        if(!['sitemapindex','urlset'].includes(type))throw Error('Unrecognized sitemap format.');
        found=true;
        $('*').filter((_i,node)=>node.name?.split(':').at(-1)==='loc').each((_i,node)=>{
          const loc=$(node).text().trim();
          try{const url=scopedURL(loc,domain.host);if(type==='sitemapindex'){maps.push(url);requiredMaps.add(url);}else urls.add(url);}catch{issues.push('An out-of-scope sitemap URL was excluded.');}
        });
      } catch(error) {issues.push(error.message);}
    }
    if(!found||urls.size===0)throw Error('No usable sitemap pages found. Existing pages were preserved.');
    if(maps.length||urls.size>maxPages)issues.push('Discovery reached its page or sitemap limit.');
    const queue=[...urls].slice(0,maxPages);
    async function worker() {
      while(queue.length) {
        available();const url=queue.shift();
        let page;
        try {
          if(!allowed(url))throw Error('Blocked by robots.txt.');
          const response=await get(url,allowed);
          page=parsePage({...response,url});
        } catch(error) {store.failPage(domainId,token,url,error.message);issues.push('One or more pages could not be fetched.');continue;}
        const stored=store.savePage(domainId,token,page);fetched++;
        if(stored.indexed_hash===page.hash && stored.embedding_model===EMBEDDING_MODEL)continue;
        try { available();const vector=await (embed?embed(page):embedPage(page,key));store.index(stored.id,token,page.hash,vector);indexed++; }
        catch(error) {store.indexFailed(stored.id,token,error.message);issues.push('One or more pages could not be indexed.');}
      }
    }
    const results=await Promise.allSettled(Array.from({length:Math.min(5,queue.length)},worker));
    const failure=results.find(r=>r.status==='rejected');if(failure)throw failure.reason;
    const message=[...new Set(issues)].join(' ');
    store.finish(domainId,token,issues.length?'Partial':'Complete',message);
    return {status:issues.length?'Partial':'Complete',fetched,indexed,message};
  } catch(error) {store.finish(domainId,token,'Failed',error.message);throw error;}
  finally {clearInterval(timer);}
}
