import React,{useEffect,useRef,useState} from 'react';
import {domainHost} from './lib/source-ownership.mjs';
type Item=Record<string,any>;
const stamp=(value:string)=>value?new Date(value).toLocaleString():'Never';
const quote=(value:string)=>"'"+value.replaceAll("'","'\\''")+"'";

export default function SiteInventory({project,onProjectChange}:{project:Item;onProjectChange:(project:Item)=>Promise<boolean>}) {
 const [domains,setDomains]=useState<Item[]>([]),[pages,setPages]=useState<Item[]>([]),[sources,setSources]=useState<Item[]>([]);
 const [selected,setSelected]=useState(''),[domain,setDomain]=useState(''),[error,setError]=useState(''),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false);
 const [competitor,setCompetitor]=useState(project.competitors[0]||''),[competitorDomain,setCompetitorDomain]=useState(''),[sourceFilter,setSourceFilter]=useState('All');
 const [page,setPage]=useState<Item|null>(null);const dialog=useRef<HTMLDialogElement>(null);
 async function reload(signal?:AbortSignal) {
  const params=new URLSearchParams({project:project.id,...(selected?{domain:selected}:{})});
  const response=await fetch('/api/inventory?'+params,{signal});const body=await response.json();
  if(!response.ok)throw Error(body.error||'Could not load inventory.');
  setDomains(body.domains);setPages(body.pages);setSources(body.sources);
 }
 useEffect(()=>{const controller=new AbortController();const load=()=>reload(controller.signal).catch(e=>{if(e.name!=='AbortError')setError(e.message);});load();
  const timer=setInterval(load,5000);return()=>{controller.abort();clearInterval(timer);};},[project.id,selected,project.competitorDomains]);
 useEffect(()=>{if(page&&!dialog.current?.open)dialog.current?.showModal();},[page]);
 async function addDomain(event:React.FormEvent) {
  event.preventDefault();setBusy(true);setError('');
  try {const host=domainHost(domain);if(!await onProjectChange({...project,ownedDomains:[...new Set([...(project.ownedDomains||[]),host])]}))throw Error('Could not save the owned domain.');
   const response=await fetch('/api/inventory?'+new URLSearchParams({project:project.id}),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:host})});
   const body=await response.json();if(!response.ok)throw Error(body.error);setDomain('');setSelected(body.domain.id);await reload();
  }catch(e:any){setError(e.message);}finally{setBusy(false);}
 }
 async function copyCommand(host:string) {
  try{await navigator.clipboard.writeText(`npm run inventory -- --project ${quote(project.id)} --domain ${quote(host)} --env .env`);setNotice('Command copied. Run it from tools/prompt-tracker.');}
  catch{setError('Clipboard unavailable. Use: npm run inventory -- --project '+quote(project.id)+' --domain '+quote(host)+' --env .env');}
 }
 async function addCompetitor(event:React.FormEvent) {
  event.preventDefault();setError('');setBusy(true);
  try {const host=domainHost(competitorDomain);const rules=project.competitorDomains||[];
   if(rules.some((r:Item)=>r.domain===host&&r.name!==competitor))throw Error('That domain is already assigned to another competitor.');
   const next=[...rules.filter((r:Item)=>!(r.domain===host&&r.name===competitor)),{name:competitor,domain:host}];
   if(await onProjectChange({...project,competitorDomains:next})){setCompetitorDomain('');setNotice('Competitor domain saved. It will classify citations; it is not crawled.');}
  }catch(e:any){setError(e.message);}finally{setBusy(false);}
 }
 async function readPage(id:number) {
  try{const response=await fetch('/api/inventory?'+new URLSearchParams({project:project.id,page:String(id)}));const body=await response.json();if(!response.ok)throw Error(body.error);setPage(body.page);}catch(e:any){setError(e.message);}
 }
 return <div className='inventory'>
  {error&&<p role='alert' className='form-error'>{error}</p>}{notice&&<p role='status'>{notice}</p>}
  <div className='summary-strip'><span><b>{domains.reduce((n,d)=>n+d.page_count,0)}</b> saved pages</span><span><b>{domains.reduce((n,d)=>n+d.indexed_count,0)}</b> indexed pages</span><span><b>{sources.length}</b> cited URLs</span></div>
  <article className='panel settings-panel'><h2>Your domains</h2><p>Add a domain or subdomain. Collection stays on that host and its www alias. Add other subdomains separately.</p>
   <form className='inventory-form' onSubmit={addDomain}><label>Domain or subdomain<input aria-label='Inventory domain' placeholder='docs.example.com' value={domain} onChange={e=>setDomain(e.target.value)} required/></label><button className='button primary' disabled={busy}>Add domain</button></form>
   {domains.length?<div className='table-wrap'><table><thead><tr><th>Domain</th><th>Pages / indexed</th><th>Refresh</th><th>Last successful refresh</th><th>Actions</th></tr></thead><tbody>{domains.map(d=><tr key={d.id}>
    <td><button className='text-button' onClick={()=>setSelected(d.id)}>{d.host}</button></td><td>{d.page_count} / {d.indexed_count}</td>
    <td><span className='pill'>{d.status}</span><small>Last attempt: {stamp(d.last_attempt)}</small>{d.error&&<small>{d.error}</small>}</td><td>{stamp(d.last_success)}</td>
    <td><button className='button ghost' onClick={()=>copyCommand(d.host)}>Copy scrape command</button></td></tr>)}</tbody></table></div>:<p>No domains added. Add the client’s domain to start.</p>}
   <p className='method-note'>Run the copied command from tools/prompt-tracker with OPENAI_API_KEY in .env. Keep the computer awake during collection. Saved pages and their index need a separate backup; the workspace JSON backup does not include them.</p>
  </article>
  <article className='panel settings-panel'><div className='panel-head'><h2>Saved pages</h2><select aria-label='Inventory domain filter' value={selected} onChange={e=>setSelected(e.target.value)}><option value=''>Select a domain</option>{domains.map(d=><option value={d.id} key={d.id}>{d.host}</option>)}</select></div>
   {pages.length?<div className='table-wrap'><table><thead><tr><th>Page</th><th>Fetched</th><th>Index</th><th>Answers citing it</th></tr></thead><tbody>{pages.map(p=><tr key={p.id}>
    <td><button className='text-button' onClick={()=>readPage(p.id)}>{p.title||p.url}</button><small>{p.url}</small></td><td>{p.fetch_status}<small>{stamp(p.fetched_at)}</small>{p.error&&<small>{p.error}</small>}</td>
    <td>{p.indexed?'Indexed':'Not indexed'}{p.index_error&&<small>{p.index_error}</small>}</td><td>{p.citations}</td></tr>)}</tbody></table></div>:<p>{selected?'No pages saved yet. Run this domain’s scrape command.':'Select a domain to inspect its pages.'}</p>}
  </article>
  <article className='panel settings-panel'><h2>Competitor domains</h2><p>These rules label cited sources. They do not start a competitor crawl.</p>
   {(project.competitors||[]).map((name:string)=><div key={name} className='inventory-rule'><strong>{name}</strong><span>{(project.competitorDomains||[]).filter((r:Item)=>r.name===name).map((r:Item)=><span className='pill' key={r.domain}>{r.domain} <button aria-label={'Remove '+r.domain+' from '+name} disabled={busy} onClick={async()=>{setBusy(true);try{await onProjectChange({...project,competitorDomains:project.competitorDomains.filter((rule:Item)=>rule!==r)});}finally{setBusy(false);}}}>×</button></span>)}{!(project.competitorDomains||[]).some((r:Item)=>r.name===name)&&<small>Domain needed to identify competitor citations</small>}</span></div>)}
   <form className='inventory-form' onSubmit={addCompetitor}><label>Competitor<select aria-label='Competitor for domain' value={competitor} onChange={e=>setCompetitor(e.target.value)}>{project.competitors.map((name:string)=><option key={name}>{name}</option>)}</select></label>
    <label>Domain<input aria-label='Competitor domain' value={competitorDomain} onChange={e=>setCompetitorDomain(e.target.value)} placeholder='competitor.com' required/></label><button className='button ghost' disabled={busy||!project.competitors.length}>Save domain</button></form>
  </article>
  <article className='panel settings-panel'><div className='panel-head'><div><h2>Most cited sources</h2><p>All recorded dates and surfaces. Each captured answer counts once per URL. Missing competitor domains can leave citations classified as third-party.</p></div>
   <select aria-label='Source ownership filter' value={sourceFilter} onChange={e=>setSourceFilter(e.target.value)}>{['All','First-party','Competitor','Third-party'].map(x=><option key={x}>{x}</option>)}</select></div>
   {sources.length?<div className='table-wrap'><table><thead><tr><th>Source URL</th><th>Owner</th><th>Answers citing it</th></tr></thead><tbody>{sources.filter(s=>sourceFilter==='All'||s.kind===sourceFilter).map(s=><tr key={s.url}><td><a href={s.url} target='_blank' rel='noreferrer'>{s.url}</a></td><td>{s.kind}{s.name&&<small>{s.name}</small>}</td><td>{s.count}</td></tr>)}</tbody></table></div>:<p>No citation URLs yet. Collect or import answers to populate this list.</p>}
  </article>
  {page&&<dialog ref={dialog} className='inventory-dialog' onClose={()=>setPage(null)}><div className='modal-head'><h2>{page.title||'Saved page'}</h2><button aria-label='Close saved page' onClick={()=>dialog.current?.close()}>×</button></div><div className='evidence-body'>
   <a href={page.url} target='_blank' rel='noreferrer'>{page.url}</a><p>Fetched: {stamp(page.fetched_at)} · Model: {page.embedding_model||'Not indexed'}</p><p>{page.description}</p><p>Canonical: {page.canonical||'Not declared'} · Robots: {page.robots||'Not declared'}</p><pre>{page.content||'No saved content. Inspect the fetch error in the page list.'}</pre>
  </div></dialog>}
 </div>;
}
