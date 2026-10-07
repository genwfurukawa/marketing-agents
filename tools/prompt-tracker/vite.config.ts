import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {workspaceStore} from './src/storage.mjs';
import {workspaceSchema} from './src/lib/validation';
const seed=JSON.parse(readFileSync(new URL('./examples/workspace.json',import.meta.url),'utf8'));
const path=fileURLToPath(new URL('./.data/workspace.sqlite',import.meta.url));
function api(server:any){const store=workspaceStore(path,seed);server.httpServer?.once('close',()=>store.close());
 server.middlewares.use('/api/workspace',async(req:any,res:any)=>{
  const json=(data:any,status=200)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
  const host=String(req.headers.host||'');if(!/^(localhost|127\.0\.0\.1)(:\d+)?$/.test(host))return json({error:'Local connections only'},403);
  if(req.headers['sec-fetch-site']==='cross-site'||(req.headers.origin&&req.headers.origin!==`http://${host}`))return json({error:'Origin rejected'},403);
  try{if(req.method==='GET')return json(store.read());if(req.method!=='PUT')return json({error:'Method not allowed'},405);
   let body='';for await(const chunk of req){body+=chunk.toString();if(Buffer.byteLength(body)>8000000)return json({error:'Workspace too large'},413);}
   let payload:any;try{payload=JSON.parse(body);}catch{return json({error:'Invalid JSON'},400);}
   const parsed=workspaceSchema.safeParse(payload.data);if(!parsed.success)return json({error:parsed.error.issues[0].message},400);
   if(!Number.isInteger(payload.version)||payload.version<0)return json({error:'Invalid version'},400);
   const version=store.save(parsed.data,payload.version);return version===null?json({error:'Another tab changed this workspace. Export current work and reload.'},409):json({version});
  }catch{return json({error:'Local storage failed'},500);}
 });}
export default defineConfig({plugins:[react(),{name:'local-workspace',configureServer:api,configurePreviewServer:api}],server:{host:'127.0.0.1'},preview:{host:'127.0.0.1'}});
