import importlib.util,json,sys,unittest
from pathlib import Path
scripts=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(scripts))
spec=importlib.util.spec_from_file_location('runner',scripts/'run.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
from extractors import extract_gemini,extract_perplexity
class RunnerTests(unittest.TestCase):
 def test_identity_changes_with_prompt_model_and_repetition(self):
  base={'projects':[{'id':'p'}],'prompts':[{'id':'d','projectId':'p','active':True,'version':1,'text':'buyer question'}]}
  routes=[{'label':'Gemini','provider':'Google','model':'test-model','search':True}]
  a=runner.digest(runner.manifest_for(base,'p',routes,1));routes[0]['model']='different';self.assertNotEqual(a,runner.digest(runner.manifest_for(base,'p',routes,1)));self.assertNotEqual(a,runner.digest(runner.manifest_for(base,'p',routes,2)))
 def test_no_silent_cross_provider_route(self):
  w={'projects':[{'id':'p'}],'prompts':[{'id':'d','projectId':'p','active':True}]}
  with self.assertRaises(ValueError):runner.manifest_for(w,'p',[{'label':'ChatGPT','provider':'Perplexity','model':'test','search':True}],1)
 def test_incomplete_has_no_completed_status(self):
  self.assertFalse(runner.complete({'status':'incomplete'},{'provider':'OpenAI'},'partial text'));self.assertFalse(runner.complete({'stop_reason':'max_tokens'},{'provider':'Anthropic'},'partial text'))
 def test_perplexity_retrieval_is_not_citation(self):
  raw={'output':[{'type':'message','content':[{'type':'output_text','text':'answer without citation'}]},{'type':'search_results','results':[{'id':'1','url':'https://example.com'}]}]}
  text,cited,sources=extract_perplexity(raw);self.assertEqual(cited,[]);self.assertEqual(len(sources),1)
 def test_google_supports_cite_only_supported_chunks(self):
  raw={'candidates':[{'content':{'parts':[{'text':'Answer'}]},'groundingMetadata':{'webSearchQueries':['q'],'groundingChunks':[{'web':{'uri':'https://one.example'}},{'web':{'uri':'https://two.example'}}],'groundingSupports':[{'groundingChunkIndices':[0]}]}}]}
  _,cited,sources,searched=extract_gemini(raw);self.assertEqual(cited,['https://one.example']);self.assertEqual(len(sources),2);self.assertTrue(searched)
if __name__=='__main__':unittest.main()
