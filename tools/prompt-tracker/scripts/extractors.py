"""Provider response extraction; retrieved sources are distinct from final citations."""
import json,re

def extract_openai(raw):
    text=[];citations=[];retrieved=[];searched=False
    for item in raw.get('output',[]):
        if item.get('type')=='web_search_call':
            searched=True;retrieved.extend((item.get('action') or {}).get('sources',[]))
        if item.get('type')=='message':
            for block in item.get('content',[]):
                if block.get('type')=='output_text':text.append(block.get('text',''))
                for ann in block.get('annotations',[]):
                    if ann.get('type')=='url_citation' and ann.get('url'):citations.append(ann['url'])
    return '\n\n'.join(text),list(dict.fromkeys(citations)),retrieved,searched

def extract_claude(raw):
    texts=[];cited=[];retrieved=[];searched=False;search_errors=[]
    for b in raw.get('content',[]):
        if b.get('type')=='text':
            texts.append(b.get('text',''))
            cited.extend(c['url'] for c in b.get('citations',[]) if c.get('url'))
        if b.get('type')=='server_tool_use' and b.get('name')=='web_search':searched=True
        if b.get('type')=='web_search_tool_result':
            content=b.get('content',[])
            if isinstance(content,list):retrieved.extend({k:v for k,v in r.items() if k!='encrypted_content'} for r in content)
            elif content.get('error_code'):search_errors.append(content['error_code'])
    return ''.join(texts),list(dict.fromkeys(cited)),retrieved,searched,search_errors

def extract_gemini(raw):
    text=raw.get('output_text','');cited=[];retrieved=[];searched=False
    for step in raw.get('steps',[]):
        if step.get('type')=='model_output':
            for content in step.get('content',[]):
                if content.get('type')=='text' and not content.get('is_thought'):text+='\n'+content.get('text','')
                for ann in content.get('annotations',[]):
                    if ann.get('url'):cited.append(ann['url'])
        if 'tool' in step.get('type','') and ('google_search' in json.dumps(step) or 'search' in step.get('name','')):searched=True
    # Older Interactions response shapes and generateContent responses.
    for output in raw.get('outputs',[]):
        if output.get('type')=='text':text+='\n'+output.get('text','')
        for ann in output.get('annotations',[]):
            if ann.get('url'):cited.append(ann['url'])
    for candidate in raw.get('candidates',[]):
        text+='\n'+'\n'.join(p.get('text','') for p in candidate.get('content',{}).get('parts',[]) if not p.get('thought'))
        gm=candidate.get('groundingMetadata',{});searched=searched or bool(gm.get('webSearchQueries'))
        chunks=gm.get('groundingChunks',[]);retrieved.extend(c.get('web',{}) for c in chunks)
        indices={i for s in gm.get('groundingSupports',[]) for i in s.get('groundingChunkIndices',[])}
        cited.extend(chunks[i]['web']['uri'] for i in indices if i<len(chunks) and chunks[i].get('web',{}).get('uri'))
    return text.strip(),list(dict.fromkeys(cited)),retrieved,searched

def extract_perplexity(response):
    texts=[]; sources=[]; annotated=[]
    for item in response.get('output',[]):
        if item.get('type')=='message':
            for block in item.get('content',[]):
                if block.get('type')=='output_text':texts.append(block.get('text',''))
                for annotation in block.get('annotations',[]):
                    url=annotation.get('url') or (annotation.get('url_citation') or {}).get('url')
                    if url:annotated.append(url)
        if item.get('type')=='search_results': sources.extend(item.get('results',[]))
    if not texts and response.get('output_text'):texts=[response['output_text']]
    text='\n\n'.join(texts).strip()
    # Returned search results are retrieved sources; count as citations only
    # when referenced by an inline source ID or a citation annotation.
    ids=set(re.findall(r'\[(?:web|page):([^\]]+)\]',text))|set(re.findall(r'\[(\d+)\]',text))
    cited=list(annotated)
    for source in sources:
        sid=str(source.get('id',''));plain=sid.split(':')[-1]
        if sid in ids or plain in ids:
            if source.get('url'):cited.append(source['url'])
    return text,list(dict.fromkeys(cited)),sources
