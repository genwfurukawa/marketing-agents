import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,statSync,existsSync,writeFileSync,mkdirSync,readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {DatabaseSync} from 'node:sqlite';
import {inventoryStore,domainHost,pageURL,citationCounts,EMBEDDING_DIMENSIONS} from '../src/inventory-store.mjs';
import {sourceOwner,registeredDomain} from '../src/lib/source-ownership.mjs';
import {parseCSV} from '../src/lib/core.mjs';
import {refreshInventory,parsePage,embeddingInput,scopedURL,isPublicIP,publicRequest} from '../scripts/inventory-crawl.mjs';

const vector=()=>Array(EMBEDDING_DIMENSIONS).fill(0.1);
function setup(t) {
 const dir=mkdtempSync(join(tmpdir(),'site-inventory-')),path=join(dir,'inventory.sqlite');
 const store=inventoryStore(path),domain=store.add('client','example.com');
 t.after(()=>{store.close();rmSync(dir,{recursive:true,force:true});});
 return {store,domain,path};
}
function site({pages=['/product'],body='Original product information.',broken=false,extraMap=false}={}) {
 return async url=>{
  const path=new URL(url).pathname;
  if(path==='/robots.txt')return {status:200,body:'User-agent: *\nSitemap: https://example.com/sitemap.xml',url};
  if(path==='/sitemap.xml')return {status:200,body:extraMap?'<sitemapindex><sitemap><loc>https://example.com/child.xml</loc></sitemap><sitemap><loc>https://example.com/missing.xml</loc></sitemap></sitemapindex>':`<urlset>${pages.map(p=>`<url><loc>https://example.com${p}</loc></url>`).join('')}</urlset>`,url};
  if(path==='/child.xml')return {status:200,body:'<urlset><url><loc>https://example.com/product</loc></url></urlset>',url};
  if(path==='/missing.xml')return {status:503,body:'',url};
  if(!pages.includes(path))return {status:404,body:'',url};
  return {status:broken?503:200,type:'text/html',body:`<html><head><title>Product</title><meta name="description" content="Product summary"></head><body><nav>Navigation</nav><main><h1>Product</h1><p>${body}</p></main></body></html>`,url};
 };
}

test('crawl persists text and a compact binary vector; unchanged refresh skips embedding',async t=>{
 const {store,domain,path}=setup(t);let calls=0;
 const embed=async()=>{calls++;return vector();};
 assert.equal((await refreshInventory(store,domain.id,{request:site(),embed})).status,'Complete');
 const page=store.page(store.pages(domain.id)[0].id);
 assert.match(page.content,/Original product/);assert.doesNotMatch(page.content,/Navigation/);
 assert.equal(page.embedding_model,'text-embedding-3-small');assert.equal(store.list('client')[0].indexed_count,1);
 await refreshInventory(store,domain.id,{request:site(),embed});assert.equal(calls,1);
 const db=new DatabaseSync(path);
 const stored=db.prepare('SELECT embedding FROM pages WHERE id=?').get(page.id).embedding;
 assert.equal(stored.byteLength,1536*4);
 assert.equal(Buffer.from(stored).readFloatLE(0),Math.fround(0.1));
 db.close();
 // A small site should not preallocate a large vector index.
 assert.ok([path,path+'-wal',path+'-shm'].filter(existsSync).reduce((bytes,file)=>bytes+statSync(file).size,0)<2_000_000);
});

test('changed content replaces one vector instead of accumulating history',async t=>{
 const {store,domain,path}=setup(t);let calls=0;
 const embed=async()=>{calls++;return vector();};
 await refreshInventory(store,domain.id,{request:site(),embed});
 const before=store.page(store.pages(domain.id)[0].id);
 await refreshInventory(store,domain.id,{request:site({body:'Changed product information.'}),embed});
 const after=store.page(before.id);assert.equal(calls,2);assert.notEqual(before.content_hash,after.content_hash);
 assert.equal(after.indexed_hash,after.content_hash);assert.equal(store.pages(domain.id).length,1);
 const db=new DatabaseSync(path);assert.equal(db.prepare('SELECT count(*) count FROM pages WHERE embedding IS NOT NULL').get().count,1);db.close();
});

test('failed or partial refresh keeps saved content and last successful time',async t=>{
 const {store,domain}=setup(t);
 await refreshInventory(store,domain.id,{request:site(),embed:async()=>vector()});
 const before=store.page(store.pages(domain.id)[0].id),success=store.domain(domain.id).last_success;
 assert.equal((await refreshInventory(store,domain.id,{request:site({broken:true}),embed:async()=>vector()})).status,'Partial');
 assert.equal(store.page(before.id).content,before.content);assert.equal(store.page(before.id).indexed_hash,before.indexed_hash);
 assert.equal(store.domain(domain.id).last_success,success);
 assert.equal((await refreshInventory(store,domain.id,{request:site({extraMap:true}),embed:async()=>vector()})).status,'Partial');
 assert.equal(store.domain(domain.id).last_success,success);
 await assert.rejects(refreshInventory(store,domain.id,{request:async url=>({url,status:404,body:''}),embed:async()=>vector()}),/No usable sitemap/);
 assert.equal(store.page(before.id).content,before.content);
});

test('indexing failure saves new text, invalidates stale vector, and retries unchanged text later',async t=>{
 const {store,domain}=setup(t);
 await refreshInventory(store,domain.id,{request:site(),embed:async()=>vector()});
 const request=site({body:'New page text'});
 assert.equal((await refreshInventory(store,domain.id,{request,embed:async()=>{throw Error('Embedding unavailable');}})).status,'Partial');
 let page=store.page(store.pages(domain.id)[0].id);assert.match(page.content,/New page text/);assert.equal(page.indexed_hash,null);
 assert.equal((await refreshInventory(store,domain.id,{request,embed:async()=>vector()})).status,'Complete');
 page=store.page(page.id);assert.equal(page.indexed_hash,page.content_hash);assert.equal(page.index_error,'');
});

test('native SQLite rejects invalid vector without replacing previous index',t=>{
 const {store,domain}=setup(t);const token=store.begin(domain.id);
 const page=store.savePage(domain.id,token,{url:'https://example.com/p',title:'P',description:'',content:'Text',hash:'hash',status:200,canonical:'',robots:''});
 store.index(page.id,token,'hash',vector());
 assert.throws(()=>store.index(page.id,token,'hash',[0.1]),/Invalid embedding/);
 assert.throws(()=>store.index(page.id,token,'hash',Array(EMBEDDING_DIMENSIONS).fill(1e100)),/Invalid embedding/);
 assert.throws(()=>store.index(page.id,token,'changed-hash',vector()),/Page changed/);
 assert.equal(store.page(page.id).indexed_hash,'hash');
 store.finish(domain.id,token,'Complete');
});

test('SQLite refresh lease prevents overlapping writers and fences an expired owner',t=>{
 const {store,domain}=setup(t);const first=store.begin(domain.id);
 assert.throws(()=>store.begin(domain.id),/already running/);
 const now=Date.now;t.mock.method(Date,'now',()=>now()+130000);
 const second=store.begin(domain.id);
 assert.throws(()=>store.failPage(domain.id,first,'https://example.com/p','failure'),/ownership lost/);
 store.finish(domain.id,second,'Failed','Interrupted');
 assert.equal(store.domain(domain.id).last_success,null);
});

test('discovery is bounded, excludes other hosts and never deletes omitted pages',async t=>{
 const {store,domain}=setup(t);
 await refreshInventory(store,domain.id,{request:site({pages:['/a','/b']}),embed:async()=>vector()});
 const result=await refreshInventory(store,domain.id,{request:site({pages:['/a','/new']}),embed:async()=>vector(),maxPages:1});
 assert.equal(result.status,'Partial');assert.equal(store.pages(domain.id).length,2);
 assert.throws(()=>scopedURL('https://competitor.com/',domain.host),/outside/);
 assert.throws(()=>scopedURL('https://docs.example.com/',domain.host),/outside/);
 assert.equal(scopedURL('https://www.example.com/a',domain.host),'https://www.example.com/a');
});

test('robots denial is visible, unsafe XML and empty content are not indexed',async t=>{
 const {store,domain}=setup(t);const request=site();let embeds=0;
 const blocked=async url=>new URL(url).pathname==='/robots.txt'?{url,status:200,body:'User-agent: *\nDisallow: /product'}:request(url);
 assert.equal((await refreshInventory(store,domain.id,{request:blocked,embed:async()=>{embeds++;return vector();}})).status,'Partial');
 assert.equal(embeds,0);assert.match(store.pages(domain.id)[0].error,/robots/);
 const xml=async url=>new URL(url).pathname==='/sitemap.xml'?{url,status:200,body:'<!DOCTYPE x [<!ENTITY x "bad">]><urlset/>'}:request(url);
 await assert.rejects(refreshInventory(store,domain.id,{request:xml,embed:async()=>vector()}),/No usable sitemap/);
 assert.throws(()=>parsePage({url:'https://example.com/',status:200,type:'text/html',body:'<script>app()</script>'}),/No readable/);
});

test('public fetch guard rejects private and mapped IPs and unsafe domain inputs',()=>{
 for(const ip of ['127.0.0.1','10.0.0.1','169.254.169.254','192.168.1.1','100.64.0.1','::1','::ffff:127.0.0.1','fc00::1','fe80::1'])assert.equal(isPublicIP(ip),false,ip);
 for(const ip of ['8.8.8.8','1.1.1.1','2606:4700:4700::1111'])assert.equal(isPublicIP(ip),true,ip);
 for(const domain of ['localhost','127.0.0.1','https://example.com/path','https://user:pass@example.com','example.com:8443'])assert.throws(()=>domainHost(domain));
 assert.equal(domainHost('https://WWW.Example.com/'),'example.com');
 assert.throws(()=>scopedURL('http://example.com/','example.com'),/outside/);
 assert.throws(()=>scopedURL('https://example.com.evil.com/','example.com'),/outside/);
});

test('one competitor has many domains; descendants match without matching lookalikes',()=>{
 const project={name:'Client',domain:'client.com',competitors:['Vanta'],competitorDomains:[{name:'Vanta',domain:'vanta.com'},{name:'Vanta',domain:'vanta-alt.com'}]};
 assert.equal(sourceOwner('https://docs.vanta.com/a',project).kind,'Competitor');
 assert.equal(sourceOwner('https://vanta-alt.com/a',project).name,'Vanta');
 assert.equal(sourceOwner('https://vanta.com.evil.com/a',project).kind,'Third-party');
 assert.equal(sourceOwner('https://docs.client.com/a',project).kind,'First-party');
 assert.equal(sourceOwner('https://docs.other-owned.com/a',{...project,ownedDomains:['other-owned.com']}).kind,'First-party');
});

test('citation counts count each captured answer once per normalized URL',()=>{
 const rows=[{status:'Captured',ownedCitations:'https://www.example.com/a?utm_source=x\nhttps://example.com/a',thirdPartyCitations:'https://example.com/a'},
  {status:'Captured',ownedCitations:'https://example.com/a#fragment'},{status:'Error',ownedCitations:'https://example.com/a'}];
 assert.equal(citationCounts(rows).get('https://example.com/a'),2);
 assert.equal(pageURL('https://example.com/a#b'),'https://example.com/a');
});

test('embedding input stays safely bounded for non-English content',()=>{
 const input=embeddingInput({title:'Overview',content:'界'.repeat(20000)});
 assert.ok(Buffer.byteLength(input)<=8003);
});

test('public fetch rejects localhost at the DNS boundary',async()=>{
 await assert.rejects(publicRequest('https://localhost/','localhost'),/public addresses/);
});

test('prefixed sitemap XML is read and missing declared children make discovery partial',async t=>{
 const {store,domain}=setup(t);const original=site({extraMap:true});
 const request=async url=>{
  if(new URL(url).pathname==='/child.xml')return {status:200,url,body:'<sm:urlset xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"><sm:url><sm:loc>https://example.com/product</sm:loc></sm:url></sm:urlset>'};
  if(new URL(url).pathname==='/missing.xml')return {status:404,url,body:''};
  return original(url);
 };
 const result=await refreshInventory(store,domain.id,{request,embed:async()=>vector()});
 assert.equal(result.status,'Partial');assert.equal(store.pages(domain.id).length,1);
 assert.equal(store.domain(domain.id).last_success,null);
});

test('inventory rows and writer ownership remain separate for two client projects',t=>{
 const {store,domain}=setup(t);const second=store.add('other-client','example.com');
 assert.notEqual(second.id,domain.id);assert.equal(store.list('client').length,1);assert.equal(store.list('other-client').length,1);
 const token=store.begin(domain.id),otherToken=store.begin(second.id);
 const page=store.savePage(domain.id,token,{url:'https://example.com/p',title:'P',description:'',content:'Text',hash:'hash',status:200,canonical:'',robots:''});
 assert.equal(store.pages(second.id).length,0);assert.equal(store.page(page.id).project_id,'client');
 assert.throws(()=>store.index(page.id,otherToken,'hash',vector()),/ownership lost/);
 store.finish(domain.id,token,'Complete');store.finish(second.id,otherToken,'Complete');
});

test('removing an owned domain revokes classification despite retained inventory history',t=>{
 const {store}=setup(t);const domain=store.add('client','former.example');
 const project={name:'Client',domain:'example.com',ownedDomains:['former.example'],competitors:[]};
 assert.equal(registeredDomain(project,domain.host),true);
 assert.equal(sourceOwner('https://docs.former.example/page',project).kind,'First-party');
 const removed={...project,ownedDomains:[]};
 assert.equal(registeredDomain(removed,domain.host),false);
 assert.ok(store.list('client').some(row=>row.host==='former.example')); // Retained history is not an ownership rule.
 assert.equal(sourceOwner('https://docs.former.example/page',removed,store.list('client').map(d=>d.host)).kind,'Third-party');
 assert.equal(sourceOwner('https://former.example/page',{...removed,competitors:['Other'],competitorDomains:[{name:'Other',domain:'former.example'}]}).kind,'Competitor');
});

test('capture import uses all explicitly owned domains without absorbing competitor sources',t=>{
 const dir=mkdtempSync(join(tmpdir(),'inventory-import-'));t.after(()=>rmSync(dir,{recursive:true,force:true}));
 const workspace={projects:[{id:'p',name:'Client',domain:'client.com',ownedDomains:['other-owned.com'],competitors:['Competitor'],competitorDomains:[{name:'Competitor',domain:'competitor.com'}]}],prompts:[{id:'q',projectId:'p',version:1,text:'Question?'}]};
 writeFileSync(join(dir,'workspace.json'),JSON.stringify(workspace));mkdirSync(join(dir,'captures'));
 writeFileSync(join(dir,'captures','capture.json'),JSON.stringify({id:'answer',prompt:workspace.prompts[0],status:'Captured',engine:'ChatGPT',provider:'BrightData',collection:'Consumer UI',completedAt:'2026-11-08T00:00:00Z',answer:'Fixture answer',citations:['https://docs.other-owned.com/a','https://competitor.com/a'],repetition:1}));
 const result=spawnSync(process.execPath,['scripts/import-captures.mjs',join(dir,'workspace.json'),join(dir,'captures'),join(dir,'answers.csv')],{cwd:new URL('../',import.meta.url),encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);
 const rows=parseCSV(readFileSync(join(dir,'answers.csv'),'utf8'));
 assert.equal(rows[0].ownedCitations,'https://docs.other-owned.com/a');assert.equal(rows[0].thirdPartyCitations,'https://competitor.com/a');
});
