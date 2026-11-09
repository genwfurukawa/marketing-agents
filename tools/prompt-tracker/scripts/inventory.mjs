import {parseArgs,parseEnv} from 'node:util';
import {readFileSync,existsSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {workspaceStore} from '../src/storage.mjs';
import {inventoryStore,domainHost} from '../src/inventory-store.mjs';
import {refreshInventory} from './inventory-crawl.mjs';

const {values}=parseArgs({options:{project:{type:'string'},domain:{type:'string'},env:{type:'string',default:'.env'},'max-pages':{type:'string',default:'200'},'dry-run':{type:'boolean',default:false}}});
let inventory;
try {
  if(!values.project||!values.domain)throw Error('Usage: npm run inventory -- --project PROJECT_ID --domain example.com [--env .env] [--max-pages 200] [--dry-run]');
  const host=domainHost(values.domain),maxPages=Number(values['max-pages']);
  if(!Number.isInteger(maxPages)||maxPages<1||maxPages>1000)throw Error('--max-pages must be between 1 and 1000.');
  const root=new URL('../',import.meta.url);
  const workspace=workspaceStore(fileURLToPath(new URL('.data/workspace.sqlite',root)),JSON.parse(readFileSync(new URL('examples/workspace.json',root),'utf8')));
  let project;try{project=workspace.read().data.projects.find(p=>p.id===values.project);}finally{workspace.close();}
  if(!project)throw Error('Unknown project ID. Copy the command from Site inventory.');
  if(![project.domain,...(project.ownedDomains||[])].filter(Boolean).some(value=>{try{return domainHost(value)===host;}catch{return false;}}))throw Error('Add this owned domain in Site inventory before running its command.');
  if(values['dry-run']) {
    console.log(`Project: ${project.name}; domain: ${host}; at most ${maxPages} pages; five workers; one local vector per page. No network requests made.`);
  } else {
    const env={...process.env,...(existsSync(values.env)?parseEnv(readFileSync(values.env,'utf8')):{})};
    if(!env.OPENAI_API_KEY)throw Error('Set OPENAI_API_KEY in the environment or .env before scraping and indexing.');
    inventory=inventoryStore(fileURLToPath(new URL('.data/inventory.sqlite',root)));
    const domain=inventory.add(project.id,host);
    const controller=new AbortController();
    const interrupt=()=>controller.abort();process.once('SIGINT',interrupt);process.once('SIGTERM',interrupt);
    try {
      const result=await refreshInventory(inventory,domain.id,{key:env.OPENAI_API_KEY,maxPages,signal:controller.signal});
      console.log(`${host}: ${result.status}; ${result.fetched} pages fetched; ${result.indexed} embeddings updated.`);
      if(result.message)console.log(result.message);
      if(result.status!=='Complete')process.exitCode=1;
    } finally {process.removeListener('SIGINT',interrupt);process.removeListener('SIGTERM',interrupt);}
  }
} catch(error) {console.error(error.message);process.exitCode=1;}
finally {inventory?.close();}
