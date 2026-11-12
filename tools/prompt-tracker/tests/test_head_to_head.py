import copy
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import head_to_head as h2h
import score
from run import digest


def example(subject='Acme',competitor='Beta'):
    project={'id':'p','name':subject,'domain':'client.example','competitors':[competitor]}
    prompt={'id':'q','projectId':'p','text':f'{subject} vs {competitor}: which should I choose?', 'group':'Comparison','version':1}
    answer={'id':'a','projectId':'p','promptId':'q','status':'Captured','text':f'{subject} and {competitor} are compared. {subject} is the better fit. I recommend {subject}.',
            'promptVersion':1,'promptText':prompt['text'],'engine':'ChatGPT','date':'2026-11-09','mentioned':False,'recommended':False,
            'brands':'Manual label','assessmentReviewed':True,'notes':'Keep my notes','checkedClaims':0,'errorClaims':0}
    pair={'competitor':competitor}
    context=h2h.context_for(project,prompt,answer,pair)
    writer={'subjectAssessment':subject+' fits the request.','competitorAssessment':competitor+' is compared.',
            'comparisonQuote':subject+' is the better fit.','recommendationQuote':'I recommend '+subject+'.',
            'headToHeadQuote':subject+' and '+competitor+' are compared.'}
    decisions={'feature_winner':'us','recommendation':'subject','head_to_head':'yes'}
    return project,prompt,answer,pair,context,writer,decisions


def jev_response(decisions):
    return {'model':h2h.JEV_MODEL,'answers':{key:{'type':'choice','choice':value} for key,value in decisions.items()}}


def openai_response(writer):
    return {'status':'completed','model':'fixture-openai','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(writer)}]}]}


class ContractTests(unittest.TestCase):
    def test_canonical_outcome_priority_and_evidence_for_two_industries(self):
        for subject,competitor in [('Acme','Beta'),('Harbor Freight Line','Ridge Air')]:
            with self.subTest(subject=subject):
                _,_,_,_,context,writer,decisions=example(subject,competitor)
                request=h2h.decision_request(context)
                parsed=h2h.parse_decisions(request,jev_response(decisions))
                result=h2h.checked_score(context,parsed,h2h.parse_writer(openai_response(writer)))
                self.assertEqual(result['outcome'],'we_win');self.assertTrue(result['recommended'])
                quote=result['evidence']['recommendationQuote']
                self.assertEqual(context['answer'][quote['start']:quote['end']],quote['text'])
                # An explicit overall recommendation overrides a weaker feature tie.
                self.assertEqual(h2h.checked_score(context,{**decisions,'feature_winner':'tie'},writer)['outcome'],'we_win')

    def test_conditional_and_balanced_answers_are_ties_not_recommendations(self):
        _,_,_,_,context,_,_=example()
        context['answer']='Use Acme for design; use Beta for automation. Choose based on your needs.'
        writer={key:None for key in h2h.WRITER_FIELDS};writer.update(comparisonQuote=context['answer'],headToHeadQuote=context['answer'])
        result=h2h.checked_score(context,{'feature_winner':'tie','recommendation':'none','head_to_head':'yes'},writer)
        self.assertEqual(result['outcome'],'tie');self.assertIsNone(result['recommendedCompany']);self.assertFalse(result['recommended'])

    def test_not_compared_is_not_a_loss_and_prose_comparison_is_tie(self):
        _,_,_,_,context,_,_=example();writer={key:None for key in h2h.WRITER_FIELDS}
        decisions={'feature_winner':'not_compared','recommendation':'none','head_to_head':'no'}
        self.assertEqual(h2h.checked_score(context,decisions,writer)['outcome'],'not_compared')
        writer['headToHeadQuote']=context['answer']
        self.assertEqual(h2h.checked_score(context,{**decisions,'head_to_head':'yes'},writer)['outcome'],'tie')

    def test_off_pair_unknown_model_missing_ids_and_invalid_choices_hold(self):
        _,_,_,_,context,_,decisions=example();request=h2h.decision_request(context)
        for response in [jev_response({**decisions,'recommendation':'other'}),{'model':'different','answers':{}},
                         {'model':h2h.JEV_MODEL,'answers':{}},jev_response({**decisions,'feature_winner':[]}),
                         jev_response({**decisions,'head_to_head':'no'})]:
            with self.subTest(response=response),self.assertRaises(ValueError):h2h.parse_decisions(request,response)

    def test_exact_quote_contract_unicode_case_whitespace_and_negatives(self):
        text='Café\n  supports α-level workflows. It does not support billing.'
        bound=h2h.locate_quote(text,'CAFÉ supports α-level workflows.')
        self.assertEqual(bound['text'],'Café\n  supports α-level workflows.')
        self.assertIsNone(h2h.locate_quote(text,'Cafe supports α-level workflows.'))
        self.assertIsNone(h2h.locate_quote(text,'It supports billing.'))
        self.assertIsNone(h2h.locate_quote(text,'Cafe\u0301 supports α-level workflows.'))

    def test_required_missing_or_invented_receipt_rejects_entire_score(self):
        _,_,_,_,context,writer,decisions=example()
        for quote in [None,'Acme is best at everything.']:
            with self.subTest(quote=quote),self.assertRaises(ValueError):h2h.checked_score(context,decisions,{**writer,'recommendationQuote':quote})
        with self.assertRaises(ValueError):h2h.checked_score(context,decisions,{**writer,'subjectAssessment':'A generic claim without an identity.'})

    def test_context_requires_exact_prompt_identity_and_configured_competitor(self):
        project,prompt,answer,pair,_,_,_=example()
        for wrong_prompt,wrong_answer,wrong_pair in [({**prompt,'group':'Discovery'},answer,pair),(prompt,{**answer,'promptVersion':2},pair),
                (prompt,{**answer,'text':''},pair),(prompt,answer,{'competitor':'Unknown'}),(prompt,answer,{'competitor':'Beta','subjectProduct':42})]:
            with self.assertRaises(ValueError):h2h.context_for(project,wrong_prompt,wrong_answer,wrong_pair)

    def test_openai_schema_no_storage_and_incomplete_outputs_hold(self):
        _,_,_,_,context,writer,decisions=example()
        payload=h2h.writer_payload(context,decisions,'fixture-model')
        self.assertIs(payload['store'],False);self.assertTrue(payload['text']['format']['strict'])
        with self.assertRaises(ValueError):h2h.parse_writer({**openai_response(writer),'status':'incomplete'})
        with self.assertRaises(ValueError):h2h.parse_writer(openai_response({**writer,'inventedField':True}))
        with self.assertRaises(ValueError):h2h.decision_request({**context,'answer':'界'*20000})


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.output=Path(self.temp.name)
        self.project,self.prompt,self.answer,self.pair,self.context,self.writer,self.decisions=example()
        self.config={'jevModel':h2h.JEV_MODEL,'openaiModel':'fixture-openai','maxRequests':20}
        self.env={'TYPESAFE_API_KEY':'fixture-typesafe-secret','OPENAI_API_KEY':'fixture-openai-secret'}
        self.job={'answerId':'a','projectId':'p','context':self.context,'pair':self.pair}

    def runner(self,cap=20):return score.Scorer(self.output,{**self.config,'maxRequests':cap},self.env,'run-fixture')

    def responses(self,url,payload,key):
        return jev_response(self.decisions) if 'typesafe.ai' in url else openai_response(self.writer)

    def test_resume_jev_done_does_not_repeat_primary_and_completed_is_reused(self):
        with patch.object(score,'post',side_effect=self.responses) as calls:
            first=self.runner(1).work(self.job);self.assertEqual(first['status'],'JevDone')
            result=self.runner(3).work(self.job);self.assertEqual(result['status'],'Scored')
            self.runner(3).work(self.job);self.assertEqual(calls.call_count,2)
        self.assertEqual(result['models']['openaiReturned'],'fixture-openai')

    def test_interrupted_submission_is_held_and_failed_evidence_does_not_create_score(self):
        with patch.object(score,'post',side_effect=self.responses):task=self.runner(1).work(self.job)
        task['status']='OpenAISubmitting';self.runner().save(task)
        with patch.object(score,'post',side_effect=AssertionError('Resubmitted')):
            self.assertEqual(self.runner().work(self.job)['status'],'SubmissionUnknown')

    def test_bad_provider_output_holds_and_secrets_are_not_persisted(self):
        with patch.object(score,'post',return_value={'model':'wrong','answers':{},'echo':self.env['TYPESAFE_API_KEY']}):
            task=self.runner().work(self.job)
        self.assertEqual(task['status'],'Hold');self.assertNotIn('score',task)
        for path in self.output.glob('*.json'):self.assertNotIn(self.env['TYPESAFE_API_KEY'],path.read_text())

    def test_shared_request_cap_across_five_workers(self):
        runner=self.runner(5);barrier=threading.Barrier(5,timeout=5);count=0;lock=threading.Lock()
        def post(*args):
            nonlocal count
            with lock:count+=1
            barrier.wait();return jev_response(self.decisions)
        with patch.object(score,'post',side_effect=post),ThreadPoolExecutor(max_workers=5) as pool:
            results=list(pool.map(runner.work,[{**self.job,'answerId':str(i)} for i in range(8)]))
        self.assertEqual(count,5);self.assertEqual(runner.state['requestsUsed'],5)
        self.assertEqual(sum(r['status']=='Scored' for r in results),0)

    def test_suggestions_preserve_reviewed_manual_fields_and_fence_changed_answers(self):
        with patch.object(score,'post',side_effect=self.responses):artifact=self.runner().work(self.job)
        workspace={'projects':[self.project],'prompts':[self.prompt],'answers':[self.answer], 'content':[], 'experiments':[]}
        path=self.output/'workspace.sqlite'
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE workspace(id INTEGER PRIMARY KEY,data TEXT,version INTEGER)')
            db.execute('INSERT INTO workspace VALUES(1,?,7)',(json.dumps(workspace),))
        self.assertEqual(score.apply_suggestions(path,'p',[artifact]),(1,0))
        current=score.read_workspace(path)['answers'][0]
        self.assertTrue(current['assessmentReviewed']);self.assertEqual(current['notes'],'Keep my notes');self.assertEqual(current['brands'],'Manual label')
        self.assertFalse(current['recommended']);self.assertIn('scoringSuggestion',current)
        self.assertEqual(score.apply_suggestions(path,'p',[artifact]),(0,0))
        with closing(sqlite3.connect(path)) as db, db:
            self.assertEqual(db.execute('SELECT version FROM workspace').fetchone()[0],8)
            workspace['answers'][0]['text']='Edited while model was running.'
            db.execute('UPDATE workspace SET data=?',(json.dumps(workspace),))
        self.assertEqual(score.apply_suggestions(path,'p',[artifact]),(0,1))
        self.assertNotIn('scoringSuggestion',score.read_workspace(path)['answers'][0])

    def test_size_limit_rolls_back_and_other_clients_are_never_modified(self):
        with patch.object(score,'post',side_effect=self.responses):artifact=self.runner().work(self.job)
        other={**self.answer,'id':'other','projectId':'other-project'}
        workspace={'projects':[self.project,{'id':'other-project','name':'Other','competitors':['Beta']}],
                   'prompts':[self.prompt],'answers':[self.answer,other]}
        path=self.output/'workspace.sqlite'
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE workspace(id INTEGER PRIMARY KEY,data TEXT,version INTEGER)')
            db.execute('INSERT INTO workspace VALUES(1,?,1)',(json.dumps(workspace),))
        oversized=copy.deepcopy(artifact);oversized['score']['subjectAssessment']='x'*8_000_000
        with self.assertRaisesRegex(ValueError,'size limit'):score.apply_suggestions(path,'p',[oversized])
        self.assertEqual(score.read_workspace(path),workspace)
        self.assertEqual(score.apply_suggestions(path,'p',[{**artifact,'answerId':'other'}]),(0,1))
        self.assertNotIn('scoringSuggestion',score.read_workspace(path)['answers'][1])

    def test_cli_preflight_and_complete_flow_with_fixture_providers(self):
        path=self.output/'workspace.sqlite';config_path=self.output/'config.json';out=self.output/'scores'
        config_path.write_text(json.dumps({**self.config,'comparisons':{'q':self.pair}}))
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE workspace(id INTEGER PRIMARY KEY,data TEXT,version INTEGER)')
            db.execute('INSERT INTO workspace VALUES(1,?,1)',(json.dumps({'projects':[self.project],'prompts':[self.prompt],'answers':[self.answer]}),))
        args=['score.py','--project','p','--config',str(config_path),'--output',str(out),'--database',str(path)]
        with patch.object(sys,'argv',args+['--dry-run']),patch.object(score,'post',side_effect=AssertionError('Dry run called provider')):
            score.main()
        self.assertFalse(out.exists())
        with patch.dict('os.environ',self.env),patch.object(sys,'argv',args),patch.object(score,'post',side_effect=self.responses) as calls:
            score.main();self.assertEqual(calls.call_count,2)
        answer=score.read_workspace(path)['answers'][0]
        self.assertIn('scoringSuggestion',answer);self.assertEqual(answer['brands'],'Manual label');self.assertTrue(answer['assessmentReviewed'])
        with patch.dict('os.environ',self.env),patch.object(sys,'argv',args),patch.object(score,'post',side_effect=AssertionError('Completed call repeated')):
            score.main()


if __name__=='__main__':unittest.main()
