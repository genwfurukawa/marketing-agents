import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {workspaceStore} from './src/storage.mjs';
import {workspaceSchema} from './src/lib/validation';
import {inventoryStore,citationCounts,pageURL,domainHost} from './src/inventory-store.mjs';
import {sourceOwner,registeredDomain} from './src/lib/source-ownership.mjs';
const seed=JSON.parse(readFileSync(new URL('./examples/workspace.json',import.meta.url),'utf8'));
const path=fileURLToPath(new URL('./.data/workspace.sqlite',import.meta.url));
function localError(req:any){const host=String(req.headers.host||'');if(!/^(localhost|127\.0\.0\.1)(:\d+)?$/.test(host))return 'Local connections only';
 if(req.headers['sec-fetch-site']==='cross-site'||(req.headers.origin&&req.headers.origin!==`http://${host}`))return 'Origin rejected';return '';}
function api(server:any){const store=workspaceStore(path,seed);const inventory=inventoryStore(fileURLToPath(new URL('./.data/inventory.sqlite',import.meta.url)));
 server.httpServer?.once('close',()=>{store.close();inventory.close();});
 server.middlewares.use('/api/inventory',async(req:any,res:any)=>{
  const json=(data:any,status=200)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
  const denied=localError(req);if(denied)return json({error:denied},403);
  try{
   const params=new URL(req.url,'http://localhost').searchParams;
   const workspace=store.read().data;const project=workspace.projects.find((p:any)=>p.id===params.get('project'));
   if(!project)return json({error:'Unknown project'},404);
   if(req.method==='GET'){
    if(params.has('page')){const page=inventory.page(Number(params.get('page')));if(!page||page.project_id!==project.id||!registeredDomain(project,inventory.domain(page.domain_id)!.host))return json({error:'Unknown page'},404);return json({page});}
    const domains=inventory.list(project.id).filter((domain:any)=>registeredDomain(project,domain.host)),domainId=params.get('domain');
    if(domainId&&!domains.some((d:any)=>d.id===domainId))return json({error:'Unknown domain'},404);
    const counts=citationCounts(workspace.answers.filter((a:any)=>a.projectId===project.id));
    const sources=[...counts].map(([url,count])=>({url,count,...sourceOwner(url,project)})).sort((a,b)=>b.count-a.count);
    return json({domains,pages:domainId?inventory.pages(domainId).map((p:any)=>({...p,citations:counts.get(pageURL(p.url))||0})):[],sources});
   }
   if(req.method!=='POST')return json({error:'Method not allowed'},405);
   let body='';for await(const chunk of req){body+=chunk.toString();if(Buffer.byteLength(body)>10000)return json({error:'Request too large'},413);}
   let input;try{input=JSON.parse(body);}catch{return json({error:'Invalid JSON'},400);}
   if(typeof input.domain!=='string')return json({error:'A domain is required'},400);
   try{const host=domainHost(input.domain);if(!registeredDomain(project,host))return json({error:'Save this domain as client-owned before creating its inventory.'},400);
    return json({domain:inventory.add(project.id,host)},201);}catch{return json({error:'Enter a valid domain or subdomain without a path or port.'},400);}
  }catch{return json({error:'Inventory storage failed'},500);}
 });
 server.middlewares.use('/api/workspace',async(req:any,res:any)=>{
  const json=(data:any,status=200)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
  const denied=localError(req);if(denied)return json({error:denied},403);
  try{if(req.method==='GET')return json(store.read());if(req.method!=='PUT')return json({error:'Method not allowed'},405);
   let body='';for await(const chunk of req){body+=chunk.toString();if(Buffer.byteLength(body)>8000000)return json({error:'Workspace too large'},413);}
   let payload:any;try{payload=JSON.parse(body);}catch{return json({error:'Invalid JSON'},400);}
   const parsed=workspaceSchema.safeParse(payload.data);if(!parsed.success)return json({error:parsed.error.issues[0].message},400);
   if(!Number.isInteger(payload.version)||payload.version<0)return json({error:'Invalid version'},400);
   const version=store.save(parsed.data,payload.version);return version===null?json({error:'Another tab changed this workspace. Export current work and reload.'},409):json({version});
  }catch{return json({error:'Local storage failed'},500);}
 });}
export default defineConfig({plugins:[react(),{name:'local-workspace',configureServer:api,configurePreviewServer:api}],server:{host:'127.0.0.1'},preview:{host:'127.0.0.1'}});
