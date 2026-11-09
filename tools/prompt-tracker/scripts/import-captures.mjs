import {readFileSync,readdirSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {toCSV} from '../src/lib/core.mjs';
import {sourceOwner} from '../src/lib/source-ownership.mjs';
const [workspacePath,capturesPath,outputPath]=process.argv.slice(2);
if(!outputPath)throw Error('Usage: node scripts/import-captures.mjs WORKSPACE.json CAPTURE_DIR OUTPUT.csv');
const input=JSON.parse(readFileSync(workspacePath,'utf8'));const workspace=input.data||input;
const rows=[];
for(const file of readdirSync(capturesPath).filter(f=>f.endsWith('.json')&&f!=='manifest.json')){
 const a=JSON.parse(readFileSync(join(capturesPath,file),'utf8'));
 if(!['Captured','Error','Incomplete'].includes(a.status))continue;
 const p=workspace.prompts.find(p=>p.id===a.prompt.id&&p.version===a.prompt.version&&p.text===a.prompt.text);
 if(!p)throw Error('Prompt version does not match this workspace: '+a.prompt.id);
 const project=workspace.projects.find(x=>x.id===p.projectId);
 const urls=(a.citations||[]).filter(u=>{try{return ['http:','https:'].includes(new URL(u).protocol);}catch{return false;}});
 const owned=url=>sourceOwner(url,project).kind==='First-party';
 rows.push({id:a.id,prompt_id:p.id,surface:a.engine,status:a.status==='Captured'?'captured':'error',date:a.completedAt,collection:a.collection||'API',provider:a.provider,model:a.model||a.requestedModel,searchBackend:a.searchBackend,search:a.searchEnabled===true?'Enabled':a.searchEnabled===false?'Disabled':'Unknown',searchPerformed:a.searchPerformed===true?'true':a.searchPerformed===false?'false':'',region:a.region||'',run:a.repetition,text:a.answer||'',ownedCitations:urls.filter(owned).join('\n'),thirdPartyCitations:urls.filter(u=>!owned(u)).join('\n'),assessmentReviewed:false,mentioned:false,recommended:false,checkedClaims:0,errorClaims:0,notes:'Recommendation labels need human review. Raw response: '+file+(a.fallbackUsed?' · API fallback after Bright Data failures':'')+(a.error?' · '+a.error:'')});
}
writeFileSync(outputPath,toCSV(rows));console.log(`Exported ${rows.length} records. Import through Answer evidence; review labels before using recommendation rates.`);
