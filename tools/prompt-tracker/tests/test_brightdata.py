"""Synthetic collection tests. No credentials, provider calls or client data."""
import copy
import json
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import brightdata as bd
import run


def route(label='ChatGPT'):
    r = {'label': label, 'provider': 'BrightData', 'datasetId': 'gd_fixture', 'country': 'US',
         'fallback': {'provider': bd.SURFACES[label][1], 'model': 'fixture-model', 'search': True,
                      'searchBackend': 'Fixture search'}}
    if label == 'ChatGPT':
        r['search'] = True
    return r


def workspace(count=1):
    return {'projects': [{'id': 'p', 'name': 'Example', 'domain': 'example.com'}],
            'prompts': [{'id': f'q{i}', 'projectId': 'p', 'text': f'Question {i}?',
                         'active': True, 'version': 1} for i in range(count)]}


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.route = route()
        self.manifest = run.manifest_for(workspace(), 'p', [self.route], 1)
        self.env = {name: 'secret-' + name for name in bd.KEYS.values()}

    def runner(self, config=None, manifest=None):
        manifest = manifest or self.manifest
        r = bd.Runner(self.out, manifest, run.digest(manifest)[:24], config or {}, self.env)
        r.wait = lambda until: None
        return r

    def task(self):
        return json.loads(next(p for p in self.out.glob('*.json') if p.name != 'manifest.json').read_text())

    def work(self, r):
        return r.work(self.manifest['prompts'][0], self.route, 1)

    def test_success_saved_snapshot_resumed_and_completed_skipped(self):
        r = self.runner({'maxRequests': 1})
        r.request = lambda *args: {'snapshot_id': 'snapshot-1'}
        self.assertEqual(self.work(r), 'Submitted')
        self.assertEqual(self.task()['brightDataAttempts'][0]['snapshotId'], 'snapshot-1')
        resumed = self.runner({'maxRequests': 10})
        calls = []
        def request(method, url, route, payload=None):
            calls.append((method, url))
            return {'status': 'ready'} if '/progress/' in url else [{'answer_text': 'A complete answer.'}]
        resumed.request = request
        self.assertEqual(self.work(resumed), 'Captured')
        self.assertTrue(all(method == 'GET' for method, _ in calls))
        self.assertEqual(self.work(resumed), 'Captured')
        self.assertEqual(len(calls), 2)
        self.assertEqual(resumed.state['requestsUsed'], 3)

    def test_three_failed_snapshots_then_matching_api_for_every_surface(self):
        for label in bd.SURFACES:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                self.out = Path(directory)
                self.route = route(label)
                self.manifest = run.manifest_for(workspace(), 'p', [self.route], 1)
                r = self.runner()
                submissions = []
                def request(method, url, route, payload=None):
                    if '/trigger?' in url:
                        submissions.append(payload)
                        return {'snapshot_id': f'snapshot-{len(submissions)}'}
                    if '/progress/' in url:
                        return {'status': 'failed'}
                    if label == 'Gemini':
                        return {'status': 'completed', 'outputs': [{'type': 'text', 'text': 'API answer'}]}
                    return {'status': 'completed', 'model': 'returned-model', 'output': [
                        {'type': 'message', 'content': [{'type': 'output_text', 'text': 'API answer'}]}]}
                r.request = request
                self.assertEqual(self.work(r), 'Captured')
                task = self.task()
                self.assertEqual(len(submissions), 3)
                self.assertEqual(task['provider'], bd.SURFACES[label][1])
                self.assertEqual(task['collection'], 'API')
                self.assertTrue(task['fallbackUsed'])
                self.assertEqual(task['answer'], 'API answer')
                self.assertEqual(len(task['brightDataAttempts']), 3)

    def test_failures_survive_restart_before_fallback(self):
        r = self.runner({'maxRequests': 2})
        r.request = lambda method, *args: {'snapshot_id': 's'} if method == 'POST' else {'status': 'failed'}
        self.assertEqual(self.work(r), 'Pending')
        self.assertEqual(len(self.task()['brightDataAttempts']), 1)
        resumed = self.runner({'maxRequests': 20})
        posts = []
        def request(method, url, route, payload=None):
            if '/trigger?' in url:
                posts.append(url)
                return {'snapshot_id': 'next'}
            if '/progress/' in url:
                return {'status': 'failed'}
            return {'status': 'completed', 'output': [{'type': 'message', 'content': [
                {'type': 'output_text', 'text': 'Recovered by API'}]}]}
        resumed.request = request
        self.assertEqual(self.work(resumed), 'Captured')
        self.assertEqual(len(posts), 2)

    def test_poll_and_download_transient_failures_never_resubmit(self):
        r = self.runner()
        responses = iter([{'snapshot_id': 's'}, bd.HTTPFailure(429, '0'), {'status': 'running'},
                          {'status': 'ready'}, {'status': 'building'}, TimeoutError(),
                          [{'answer_text': 'Recovered snapshot'}]])
        methods = []
        def request(method, *args):
            methods.append(method)
            value = next(responses)
            if isinstance(value, Exception):
                raise value
            return value
        r.request = request
        self.assertEqual(self.work(r), 'Captured')
        self.assertEqual(methods.count('POST'), 1)
        self.assertEqual(len(self.task()['brightDataAttempts']), 1)

    def test_unknown_submission_never_repeated_and_interrupted_marker_held(self):
        r = self.runner()
        def request(*args):
            raise TimeoutError('secret-BRIGHTDATA_API_KEY')
        r.request = request
        self.assertEqual(self.work(r), 'SubmissionUnknown')
        resumed = self.runner()
        resumed.request = lambda *args: self.fail('Unknown submission repeated')
        self.assertEqual(self.work(resumed), 'SubmissionUnknown')
        task = self.task()
        task['status'] = 'Submitting'
        resumed.save(task)
        self.assertEqual(self.work(resumed), 'SubmissionUnknown')
        self.assertFalse(task.get('fallbackUsed', False))
        for file in self.out.glob('*.json'):
            self.assertNotIn(self.env['BRIGHTDATA_API_KEY'], file.read_text())

    def test_bad_rows_retry_then_fallback_without_scoring_them(self):
        r = self.runner()
        downloads = iter([[{'error_code': 'blocked'}], [{'answer_text': ''}],
                          [{'answer_text': 'Just a moment'}]])
        def request(method, url, route, payload=None):
            if '/trigger?' in url:
                return {'snapshot_id': 's'}
            if '/progress/' in url:
                return {'status': 'ready'}
            if '/snapshot/' in url:
                return next(downloads)
            return {'status': 'completed', 'output_text': ''}
        r.request = request
        self.assertEqual(self.work(r), 'Error')
        self.assertEqual(len(self.task()['brightDataAttempts']), 3)
        self.assertEqual(len(self.task()['apiAttempts']), 3)
        self.assertNotIn('answer', self.task())

    def test_malformed_source_lists_fail_collection_attempt_instead_of_aborting_run(self):
        r = self.runner()
        downloads = iter([[{'answer_text': 'Answer', 'citations': 42}],
                          [{'answer_text': 'Another answer', 'sources': {'url': 'https://example.com'}}],
                          [{'answer_text': 'Third answer', 'search_sources': 'invalid'}]])
        def request(method, url, route, payload=None):
            if '/trigger?' in url:
                return {'snapshot_id': 's'}
            if '/progress/' in url:
                return {'status': 'ready'}
            if '/snapshot/' in url:
                return next(downloads)
            return {'status': 'completed', 'output': [{'type': 'message', 'content': [
                {'type': 'output_text', 'text': 'Valid API answer'}]}]}
        r.request = request
        self.assertEqual(self.work(r), 'Captured')
        task = self.task()
        self.assertEqual(task['answer'], 'Valid API answer')
        self.assertEqual(len(task['brightDataAttempts']), 3)
        self.assertEqual(task['brightDataAttempts'][0]['raw'][0]['citations'], 42)

    def test_five_workers_and_shared_request_cap(self):
        manifest = run.manifest_for(workspace(12), 'p', [self.route], 1)
        r = self.runner({'maxRequests': 5}, manifest)
        barrier = threading.Barrier(5, timeout=5)
        active = 0
        peak = 0
        lock = threading.Lock()
        def request(*args):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            barrier.wait()
            with lock:
                active -= 1
            return {'snapshot_id': 's'}
        r.request = request
        with ThreadPoolExecutor(max_workers=bd.MAX_CONCURRENT_TASKS) as pool:
            results = list(pool.map(lambda p: r.work(p, self.route, 1), manifest['prompts']))
        self.assertEqual(peak, 5)
        self.assertEqual(r.state['requestsUsed'], 5)
        self.assertEqual(results.count('Captured'), 0)
        self.assertEqual(len(list(self.out.glob('*.json'))), 13)

    def test_lock_rejects_second_runner_and_releases_after_failure(self):
        with self.assertRaisesRegex(RuntimeError, 'Another runner'):
            with bd.output_lock(self.out), bd.output_lock(self.out):
                pass
        with bd.output_lock(self.out):
            pass

    def test_identity_changes_and_missing_fallback_key_fails_before_collection(self):
        changed = copy.deepcopy(self.manifest)
        changed['providers'][0]['fallback']['model'] = 'another-model'
        self.assertNotEqual(run.digest(changed), run.digest(self.manifest))
        self.runner()
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            self.runner(manifest=changed)
        del self.env['OPENAI_API_KEY']
        with self.assertRaisesRegex(ValueError, 'Missing OPENAI_API_KEY'):
            self.runner()

    def test_payloads_match_surface_and_do_not_offer_claude(self):
        for label in bd.SURFACES:
            r = route(label)
            bd.validate_route(r)
            payload = bd.payload_for('Question?', r)[0]
            self.assertEqual(payload['prompt'], 'Question?')
            self.assertEqual(payload['country'], 'US')
            if label == 'ChatGPT':
                self.assertTrue(payload['web_search'])
                self.assertEqual(payload['additional_prompt'], '')
            else:
                self.assertEqual(payload['index'], 1)
                self.assertNotIn('web_search', payload)
        with self.assertRaisesRegex(ValueError, 'not Claude'):
            bd.validate_route({'label': 'Claude'})

    def test_citations_are_not_inferred_from_retrieved_sources(self):
        text, cited, sources = bd.extract_row({'answer_text': 'Short, valid answer.', 'citations': [
            {'url': 'https://cited.example'}, {'url': 'https://unused.example', 'cited': False}],
            'search_sources': [{'url': 'https://retrieved.example'}]})
        self.assertEqual(cited, ['https://cited.example'])
        self.assertEqual(len(sources), 1)
        with self.assertRaises(ValueError):
            bd.extract_row({'error': 'blocked', 'answer_text': text})

    def test_retry_after_is_saved_and_secrets_redacted(self):
        r = self.runner()
        task = {'id': 'fixture', 'raw': self.env['OPENAI_API_KEY']}
        r.defer(task, bd.HTTPFailure(429, '120'), 1)
        import time
        self.assertGreater(task['nextAttemptAt'], time.time() + 115)
        self.assertNotIn(self.env['OPENAI_API_KEY'], (self.out / 'fixture.json').read_text())

    def test_explicit_rejections_reach_fallback(self):
        for code in (401, 429):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as directory:
                self.out = Path(directory)
                r = self.runner()
                def request(method, url, route, payload=None):
                    if '/trigger?' in url:
                        raise bd.HTTPFailure(code)
                    return {'status': 'completed', 'output': [{'type': 'message', 'content': [
                        {'type': 'output_text', 'text': 'Fallback after unavailable scraper'}]}]}
                r.request = request
                self.assertEqual(self.work(r), 'Captured')
                self.assertTrue(self.task()['fallbackUsed'])
                self.assertEqual(len(self.task()['brightDataAttempts']), 3)

    def test_repeated_poll_errors_keep_same_snapshot(self):
        r = self.runner()
        responses = iter([{'snapshot_id': 's'}, bd.HTTPFailure(503), bd.HTTPFailure(503),
                          bd.HTTPFailure(503), {'status': 'ready'}, [{'answer_text': 'Recovered'}]])
        methods = []
        def request(method, *args):
            methods.append(method)
            value = next(responses)
            if isinstance(value, Exception):
                raise value
            return value
        r.request = request
        self.assertEqual(self.work(r), 'Captured')
        self.assertEqual(methods.count('POST'), 1)
        self.assertEqual(len(self.task()['brightDataAttempts']), 1)

    def test_post_server_error_is_held_without_resubmission(self):
        r = self.runner()
        calls = []
        def request(*args):
            calls.append(args)
            raise bd.HTTPFailure(502)
        r.request = request
        self.assertEqual(self.work(r), 'SubmissionUnknown')
        self.assertEqual(self.work(self.runner()), 'SubmissionUnknown')
        self.assertEqual(len(calls), 1)

    def test_expired_snapshot_is_downloaded_on_resume_if_ready(self):
        r = self.runner({'maxRequests': 1})
        r.request = lambda *args: {'snapshot_id': 's'}
        self.work(r)
        task = self.task()
        task['brightDataAttempts'][0]['submittedAt'] = 0
        r.save(task)
        resumed = self.runner({'maxRequests': 3})
        def request(method, url, route, payload=None):
            self.assertEqual(method, 'GET')
            return {'status': 'ready'} if '/progress/' in url else [{'answer_text': 'Finished while asleep'}]
        resumed.request = request
        self.assertEqual(self.work(resumed), 'Captured')
        self.assertEqual(len(self.task()['brightDataAttempts']), 1)

    def test_expired_snapshot_still_running_fails_only_after_progress_check(self):
        r = self.runner({'maxRequests': 1})
        r.request = lambda *args: {'snapshot_id': 's'}
        self.work(r)
        task = self.task()
        task['brightDataAttempts'][0]['submittedAt'] = 0
        r.save(task)
        resumed = self.runner({'maxRequests': 3})
        calls = []
        def request(method, url, route, payload=None):
            calls.append(method)
            return {'status': 'running'} if method == 'GET' else {'snapshot_id': 'next'}
        resumed.request = request
        self.work(resumed)
        self.assertEqual(calls, ['GET', 'POST'])
        self.assertEqual(self.task()['brightDataAttempts'][0]['status'], 'Error')
        self.assertEqual(self.task()['brightDataAttempts'][1]['snapshotId'], 'next')

    def test_truncated_http_response_is_retried_on_same_snapshot(self):
        import http.client
        from unittest.mock import MagicMock
        r = self.runner()
        def response(value):
            context = MagicMock()
            context.__enter__.return_value.read.return_value = json.dumps(value).encode()
            return context
        truncated = MagicMock()
        truncated.__enter__.return_value.read.side_effect = http.client.IncompleteRead(b'{"status":')
        with patch.object(bd.urllib.request, 'urlopen', side_effect=[
                response({'snapshot_id': 's'}), truncated, response({'status': 'ready'}),
                response([{'answer_text': 'Recovered transport'}])]) as calls:
            self.assertEqual(self.work(r), 'Captured')
        self.assertEqual(sum(call.args[0].method == 'POST' for call in calls.call_args_list), 1)

    def test_truncated_post_is_held(self):
        import http.client
        r = self.runner()
        with patch.object(bd.urllib.request, 'urlopen', side_effect=http.client.BadStatusLine('truncated')):
            self.assertEqual(self.work(r), 'SubmissionUnknown')

    def test_api_attempt_budget_and_interrupted_fallback_survive_restart(self):
        r = self.runner({'maxRequests': 4})
        def request(method, url, route, payload=None):
            if '/trigger?' in url:
                raise bd.HTTPFailure(429)
            return {'status': 'incomplete', 'output': []}
        r.request = request
        self.assertEqual(self.work(r), 'Pending')
        self.assertEqual(len(self.task()['apiAttempts']), 1)
        resumed = self.runner({'maxRequests': 10})
        resumed.request = lambda *args: []  # Malformed responses stay unscored.
        self.assertEqual(self.work(resumed), 'Error')
        self.assertEqual(len(self.task()['apiAttempts']), 3)
        self.assertEqual(resumed.state['requestsUsed'], 6)
        task = self.task()
        task['status'] = 'FallbackSubmitting'
        resumed.save(task)
        resumed.request = lambda *args: self.fail('Interrupted fallback repeated')
        self.assertEqual(self.work(resumed), 'SubmissionUnknown')

    def test_cli_five_worker_cohort_completes_and_resumes_without_network(self):
        from types import SimpleNamespace
        manifest = run.manifest_for(workspace(7), 'p', [self.route], 1)
        args = SimpleNamespace(output=str(self.out), env=None, dry_run=False)
        def request(runner, method, url, route, payload=None):
            if '/trigger?' in url:
                return {'snapshot_id': 's'}
            if '/progress/' in url:
                return {'status': 'ready'}
            return [{'answer_text': 'Fixture capture'}]
        with patch.dict('os.environ', self.env), patch.object(bd.Runner, 'request', request):
            self.assertEqual(bd.run_cohort(args, {}, manifest, run.digest(manifest)[:24]), 0)
        with patch.dict('os.environ', self.env), patch.object(bd.Runner, 'request', side_effect=AssertionError('Repeated completed run')):
            self.assertEqual(bd.run_cohort(args, {}, manifest, run.digest(manifest)[:24]), 0)

    def test_cli_import_preserves_actual_route_and_skips_pending(self):
        import csv
        workspace_path = self.out / 'workspace.fixture'
        workspace_path.write_text(json.dumps(workspace()))
        captures = self.out / 'captures'
        captures.mkdir()
        base = {'prompt': self.manifest['prompts'][0], 'engine': 'ChatGPT', 'repetition': 1,
                'completedAt': '2026-11-08T12:00:00Z', 'answer': 'Fixture answer', 'citations': []}
        for status, provider, collection in [('Captured', 'BrightData', 'Consumer UI'),
                                              ('Captured', 'OpenAI', 'API'), ('Pending', 'BrightData', 'Consumer UI')]:
            identity = provider + '-' + status
            (captures / (identity + '.json')).write_text(json.dumps({**base, 'id': identity,
                'status': status, 'provider': provider, 'collection': collection, 'fallbackUsed': provider == 'OpenAI'}))
        output = self.out / 'answers.csv'
        subprocess.run(['node', str(SCRIPTS / 'import-captures.mjs'), str(workspace_path),
                        str(captures), str(output)], check=True, capture_output=True)
        with output.open() as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 2)
        self.assertEqual({row['collection'] for row in rows}, {'API', 'Consumer UI'})
        self.assertTrue(all(row['assessmentReviewed'] == 'false' for row in rows))
        self.assertIn('API fallback', next(row['notes'] for row in rows if row['provider'] == 'OpenAI'))

    def test_actual_http_payload_and_auth_against_local_fixture_server(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        import urllib.request
        received = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append((self.path, self.headers['Authorization'],
                                 json.loads(self.rfile.read(int(self.headers['Content-Length'])))))
                self.respond({'snapshot_id': 'fixture-snapshot'})
            def do_GET(self):
                self.respond({'status': 'ready'} if '/progress/' in self.path else [
                    {'answer_text': 'An answer from the fixture server.', 'citations': [{'url': 'https://example.com/source'}]}])
            def respond(self, value):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(value).encode())
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            r = self.runner()
            with patch.object(bd, 'BASE', f'http://127.0.0.1:{server.server_port}/datasets/v3'):
                self.assertEqual(self.work(r), 'Captured')
            self.assertEqual(received[0][1], 'Bearer ' + self.env['BRIGHTDATA_API_KEY'])
            self.assertEqual(received[0][2], bd.payload_for('Question 0?', self.route))
            self.assertIn('dataset_id=gd_fixture', received[0][0])
            self.assertEqual(self.task()['citations'], ['https://example.com/source'])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
