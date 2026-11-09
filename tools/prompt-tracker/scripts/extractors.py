"""Provider response extraction; retrieved sources are distinct from final citations."""
import json,re
from html.parser import HTMLParser
from urllib.parse import urlparse


class _CitationChips(HTMLParser):
    """KnitKnot's ChatGPT/Perplexity chip shapes, read without a browser or LLM."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.urls = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        payload = attrs.get('data-assistant-sources-payload')
        if payload:
            try:
                items = json.loads(payload)
                if isinstance(items, list):
                    self.urls.extend(item['url'] for item in items if isinstance(item, dict) and isinstance(item.get('url'), str))
            except ValueError:
                pass  # Optional chip metadata is unusable; don't invent citations.
        if attrs.get('data-pplx-citation-url'):
            self.urls.append(attrs['data-pplx-citation-url'])
        if tag == 'a' and any(pill for _, pill in self.stack) and attrs.get('href'):
            self.urls.append(attrs['href'])
        if tag not in self.VOID:
            self.stack.append((tag, attrs.get('data-testid') == 'webpage-citation-pill'))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def extract_brightdata_sources(row):
    """Normalize KnitKnot's source fields/chips while preserving cited vs retrieved.

    Explicit citation fields, cited flags and visible citation chips establish
    citations. Unbound search results remain retrieved sources only. The original
    response stays in the capture record.
    """
    sources = {}

    def add(source, cited=False):
        if not isinstance(source, dict) or not isinstance(source.get('url'), str):
            return
        url = source['url'].strip()
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
                return
            domain = parsed.hostname.removeprefix('www.')
        except ValueError:
            return
        if url not in sources:
            sources[url] = {'url': url, 'title': source.get('title') if isinstance(source.get('title'), str) else '',
                            'domain': domain, 'position': len(sources) + 1, 'cited': False}
        sources[url]['cited'] = sources[url]['cited'] or cited
        if source.get('id') is not None:
            sources[url]['id'] = source['id']

    for field in ('citations', 'search_sources', 'sources'):
        for source in row.get(field) or []:
            if isinstance(source, dict):
                add(source, source.get('cited') is not False if field == 'citations' else source.get('cited') is True)
    page = row.get('answer_html')
    if isinstance(page, str):
        chips = _CitationChips()
        try:
            chips.feed(page)
            chips.close()
        except (ValueError, AssertionError):
            chips.urls = []  # An unusable optional HTML field does not invalidate structured citations.
        for url in chips.urls:
            add({'url': url}, True)
    return [s['url'] for s in sources.values() if s['cited']], [s for s in sources.values() if not s['cited']]

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
        indices={i for s in gm.get('groundingSupports',[]) for i in s.get('groundingChunkIndices',[]) if type(i) is int and i>=0}
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
