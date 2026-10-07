#!/usr/bin/env python3
"""Independent API observations with immutable run identity and resumable capture.
Uses Python standard library. No brand-specific scoring or automatic routing fallback.
"""
import argparse,datetime,hashlib,json,os,time,urllib.error,urllib.request
from pathlib import Path
from extractors import extract_openai,extract_claude,extract_gemini,extract_perplexity

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def env_file(path):
    env=dict(os.environ)
    if path:
        for line in Path(path).read_text().splitlines():
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line:continue
            k,v=line.removeprefix('export ').split('=',1);env[k.strip()]=v.strip().strip('\"\x27')
    return env

def manifest_for(workspace,project,providers,repetitions):
    if not any(p['id']==project for p in workspace['projects']):raise ValueError('Unknown project ID')
    prompts=[p for p in workspace['prompts'] if p['projectId']==project and p['active']]
    if not prompts:raise ValueError('No active prompts')
    if not isinstance(repetitions,int) or repetitions<1:raise ValueError('Repetitions must be a positive integer')
    labels={'ChatGPT','Gemini','Claude','Perplexity'}
    if len({p['label'] for p in providers})!=len(providers):raise ValueError('Duplicate provider labels')
    for p in providers:
        if p['label'] not in labels:raise ValueError('Unknown surface')
        expected={'ChatGPT':'OpenAI','Claude':'Anthropic','Gemini':'Google','Perplexity':'Perplexity'}[p['label']]
        if p['provider']!=expected and not(p['label']=='Gemini' and p['provider']=='Perplexity'):raise ValueError('Unsupported explicit route')
        if not p.get('model') or p['model'].startswith('REPLACE_'):raise ValueError('Replace the example model placeholder with an available exact model ID')
        if 'search' not in p:raise ValueError('Search setting is required')
    return {'project':project,'prompts':prompts,'providers':providers,'repetitions':repetitions}

def payload_for(prompt,route):
    model=route['model'];search=route['search'];provider=route['provider'];limit=route.get('maxOutputTokens',6000)
    if provider=='OpenAI':return 'https://api.openai.com/v1/responses',{'model':model,'input':prompt,'max_output_tokens':limit,**({'tools':[{'type':'web_search'}],'include':['web_search_call.action.sources']} if search else {})}
    if provider=='Anthropic':return 'https://api.anthropic.com/v1/messages',{'model':model,'max_tokens':limit,'messages':[{'role':'user','content':prompt}],**({'tools':[{'type':'web_search_20250305','name':'web_search','max_uses':5}]} if search else {})}
    if provider=='Google':return 'https://generativelanguage.googleapis.com/v1beta/interactions',{'model':model,'input':prompt,'generation_config':{'max_output_tokens':limit},**({'tools':[{'type':'google_search'}]} if search else {})}
    return 'https://api.perplexity.ai/v1/agent',{'model':model,'input':prompt,'max_output_tokens':limit,**({'tools':[{'type':'web_search'}]} if search else {})}

def complete(raw,route,text):
    if not text.strip():return False
    if route['provider'] in ['OpenAI','Perplexity']:return raw.get('status')=='completed'
    if route['provider']=='Anthropic':return raw.get('stop_reason')=='end_turn'
    return raw.get('status')=='completed' or any(c.get('finishReason')=='STOP' for c in raw.get('candidates',[]))

def redacted(value,secrets):
    s=json.dumps(value,ensure_ascii=False,indent=2)
    for key in secrets:
        if key:s=s.replace(key,'[REDACTED]')
    return s+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workspace',required=True);ap.add_argument('--config',required=True);ap.add_argument('--project',required=True);ap.add_argument('--output',required=True);ap.add_argument('--env');ap.add_argument('--dry-run',action='store_true');args=ap.parse_args()
    workspace=json.loads(Path(args.workspace).read_text());workspace=workspace.get('data',workspace);config=json.loads(Path(args.config).read_text());routes=config['providers'];manifest=manifest_for(workspace,args.project,routes,config.get('repetitions',1));run_id=digest(manifest)[:24]
    expected=len(manifest['prompts'])*len(routes)*manifest['repetitions'];cap=config.get('maxRequests',expected)
    if not isinstance(cap,int) or cap<1:raise SystemExit('maxRequests must be positive')
    print(f'{expected} results requested; HTTP request cap {cap}; run {run_id}. A new output directory creates a new round.')
    if args.dry_run:return
    env=env_file(args.env);secrets=[v for k,v in env.items() if ('KEY' in k or 'PASSWORD' in k) and v];keys={}
    for route in routes:
        name=route.get('keyEnv') or {'OpenAI':'OPENAI_API_KEY','Anthropic':'ANTHROPIC_API_KEY','Google':'GEMINI_API_KEY','Perplexity':'PERPLEXITY_API_KEY'}[route['provider']]
        key=env.get(name) or (env.get('GOOGLE_GENAI_API_KEY') if name=='GEMINI_API_KEY' else None)
        if not key:raise SystemExit(f'Missing {name}; configure it or remove this route for an explicit partial run.')
        keys[route['label']]=key
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);mp=out/'manifest.json'
    if mp.exists() and json.loads(mp.read_text())['id']!=run_id:raise SystemExit('Run configuration changed. Use a new output directory.')
    state=json.loads(mp.read_text()) if mp.exists() else {'id':run_id,'createdAt':now(),'manifest':manifest,'requestsUsed':0}
    def save_state():mp.write_text(json.dumps(state,indent=2)+'\n')
    save_state();errors=0
    for p in manifest['prompts']:
        for route in routes:
            for rep in range(1,manifest['repetitions']+1):
                identity=digest({'run':run_id,'prompt':p,'route':route,'repetition':rep})[:24];file=out/(identity+'.json')
                if file.exists() and json.loads(file.read_text()).get('status')=='Captured':continue
                # Retain failures when explicitly resuming; never discard earlier evidence.
                if file.exists():
                    archive=out/'attempts';archive.mkdir(exist_ok=True);file.rename(archive/(identity+'-'+str(time.time_ns())+'.json'))
                result={'id':identity,'runId':run_id,'prompt':p,'engine':route['label'],'provider':route['provider'],'collection':'API','requestedModel':route['model'],'searchEnabled':route['search'],'searchBackend':route.get('searchBackend','Not specified'),'repetition':rep,'requestedAt':now(),'status':'Error'}
                url,payload=payload_for(p['text'],route);key=keys[route['label']];headers={'Content-Type':'application/json'}
                if route['provider']=='Anthropic':headers.update({'x-api-key':key,'anthropic-version':'2023-06-01'})
                elif route['provider']=='Google':headers['x-goog-api-key']=key
                else:headers['Authorization']='Bearer '+key
                try:
                    raw=None
                    for attempt in range(3):
                        if state['requestsUsed']>=cap:raise RuntimeError('Request cap reached. Raise maxRequests explicitly to resume.')
                        state['requestsUsed']+=1;save_state()
                        try:
                            req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers)
                            with urllib.request.urlopen(req,timeout=240) as response:raw=json.load(response)
                            break
                        except urllib.error.HTTPError as e:
                            if e.code in [429,500,502,503,529] and attempt<2:time.sleep(min(30,10*(attempt+1)));continue
                            raise RuntimeError(f'Provider HTTP {e.code}') from None
                    if route['provider']=='OpenAI':text,cited,sources,searched=extract_openai(raw)
                    elif route['provider']=='Anthropic':text,cited,sources,searched,search_errors=extract_claude(raw);result['searchErrors']=search_errors
                    elif route['provider']=='Google':text,cited,sources,searched=extract_gemini(raw)
                    else:text,cited,sources=extract_perplexity(raw);searched=bool(sources)
                    result.update({'status':'Captured' if complete(raw,route,text) else 'Incomplete','answer':text,'citations':cited,'retrievedSources':sources,'searchPerformed':searched,'model':raw.get('model',raw.get('modelVersion',route['model'])),'raw':raw})
                    if result['status']!='Captured':errors+=1
                except Exception as e:result['error']=str(e)[:300];errors+=1
                result['completedAt']=now();file.write_text(redacted(result,secrets));print(f"{route['label']} {p['id']} v{p['version']} repetition {rep}: {result['status']}",flush=True)
    print(f'Finished with {errors} failed/incomplete results. HTTP requests used: {state["requestsUsed"]}/{cap}.')
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
