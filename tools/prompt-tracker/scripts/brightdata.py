"""Five local workers: Bright Data first, then an explicitly configured API route.

Each capture file is also its durable task state. No scheduler or external queue.
"""
import datetime
import http.client
import json
import os
import re
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from email.utils import parsedate_to_datetime
from pathlib import Path

MAX_CONCURRENT_TASKS = 5
BRIGHTDATA_ATTEMPTS = 3
API_ATTEMPTS = 3
SNAPSHOT_TIMEOUT_SECONDS = 1200
BASE = 'https://api.brightdata.com/datasets/v3'
SURFACES = {
    'ChatGPT': ('https://chatgpt.com/', 'OpenAI'),
    'Gemini': ('https://gemini.google.com/', 'Google'),
    'Perplexity': ('https://www.perplexity.ai', 'Perplexity'),
}
KEYS = {'BrightData': 'BRIGHTDATA_API_KEY', 'OpenAI': 'OPENAI_API_KEY',
        'Google': 'GEMINI_API_KEY', 'Perplexity': 'PERPLEXITY_API_KEY'}
WAITING = {'building', 'running', 'pending', 'collecting', 'scheduled'}
TERMINAL = {'Captured', 'Error', 'SubmissionUnknown'}
PROVIDER_ERRORS = (
    'Something went wrong while generating the response',
    'Something went wrong. Please try again', "We've encountered an issue",
    'Enable JavaScript and cookies to continue', 'Verifying you are human', 'Just a moment',
)


def validate_route(route):
    if route['label'] not in SURFACES:
        raise ValueError('Bright Data supports ChatGPT, Gemini and Perplexity, not Claude.')
    if not re.fullmatch(r'gd_[A-Za-z0-9]+', route.get('datasetId', '')):
        raise ValueError('Bright Data requires a datasetId from the scraper dashboard.')
    if not isinstance(route.get('country'), str) or not route['country'].strip():
        raise ValueError('Bright Data requires an explicit country.')
    if route['label'] == 'ChatGPT' and not isinstance(route.get('search'), bool):
        raise ValueError('ChatGPT requires an explicit boolean search setting.')
    if route['label'] != 'ChatGPT' and 'search' in route:
        raise ValueError('Only the ChatGPT scraper exposes a web_search switch; omit search for other scrapers.')
    fallback = route.get('fallback', {})
    if fallback.get('provider') != SURFACES[route['label']][1]:
        raise ValueError('Fallback must use the matching surface API provider.')
    if not fallback.get('model') or fallback['model'].startswith('REPLACE_'):
        raise ValueError('Replace the fallback model placeholder with an available exact model ID.')
    if not isinstance(fallback.get('search'), bool) or not fallback.get('searchBackend'):
        raise ValueError('Fallback requires search and searchBackend settings.')


def payload_for(prompt, route):
    item = {'url': SURFACES[route['label']][0], 'prompt': prompt, 'country': route['country']}
    if route['label'] == 'ChatGPT':
        item.update(web_search=route['search'], additional_prompt='')
    else:
        item['index'] = 1
    return [item]


def extract_row(row):
    """Capture text and explicit citations only; leave recommendation scoring alone."""
    if not isinstance(row, dict) or row.get('error') or row.get('error_code'):
        raise ValueError('Bright Data returned an error record.')
    text = next((row[k].strip() for k in ('answer_text_markdown', 'answer_text',
                'exported_markdown', 'answer_text_raw') if isinstance(row.get(k), str) and row[k].strip()), '')
    if not text:
        raise ValueError('Bright Data returned no answer text.')
    if any(text.startswith(marker) for marker in PROVIDER_ERRORS):
        raise ValueError('Bright Data returned a provider error page.')
    for key in ('citations', 'search_sources', 'sources'):
        if row.get(key) is not None and not isinstance(row[key], list):
            raise ValueError('Bright Data returned an invalid ' + key + ' list.')
    citations = []
    for source in row.get('citations') or []:
        if isinstance(source, dict) and source.get('cited') is not False:
            url = source.get('url')
            if isinstance(url, str) and urllib.parse.urlparse(url).scheme in ('http', 'https'):
                citations.append(url)
    sources = [s for key in ('search_sources', 'sources') for s in row.get(key, []) or []
               if isinstance(s, dict)]
    return text, list(dict.fromkeys(citations)), sources


def atomic_json(path, value, secrets):
    from run import redacted
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w') as file:
            file.write(redacted(value, secrets))
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
        if os.name != 'nt':
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def output_lock(out):
    """OS releases this lock on exit or crash; a second runner cannot double-submit."""
    with (out / '.runner.lock').open('a+b') as file:
        if os.name == 'nt':
            import msvcrt
            file.write(b'0'); file.flush(); file.seek(0)
            acquire = lambda: msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
            release = lambda: (file.seek(0), msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1))
        else:
            import fcntl
            acquire = lambda: fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            release = lambda: fcntl.flock(file, fcntl.LOCK_UN)
        try:
            acquire()
        except OSError:
            raise RuntimeError('Another runner owns this output folder.') from None
        try:
            yield
        finally:
            release()


class Pause(Exception):
    """Keep the task resumable, without treating missing evidence as a failure."""


class HTTPFailure(Exception):
    def __init__(self, code, retry_after=None):
        self.code, self.retry_after = code, retry_after
        super().__init__(f'Provider HTTP {code}')


class Runner:
    def __init__(self, out, manifest, run_id, config, env):
        self.out, self.manifest, self.run_id = out, manifest, run_id
        self.cap = config.get('maxRequests', 1000)
        self.poll_interval = config.get('pollIntervalSeconds', 15)
        self.max_seconds = config.get('maxRunSeconds', 3600)
        for name, value in [('maxRequests', self.cap), ('pollIntervalSeconds', self.poll_interval),
                            ('maxRunSeconds', self.max_seconds)]:
            if type(value) is not int or value < 1:
                raise ValueError(name + ' must be a positive integer')
        self.deadline = time.monotonic() + self.max_seconds
        self.stop = threading.Event()
        self.mutex = threading.Lock()
        self.keys = {}
        for route in manifest['providers']:
            for r in (route, route['fallback']):
                name = r.get('keyEnv') or KEYS[r['provider']]
                key = env.get(name) or (env.get('GOOGLE_GENAI_API_KEY') if name == 'GEMINI_API_KEY' else None)
                if not key:
                    raise ValueError('Missing ' + name + '; primary and fallback keys are required before starting.')
                self.keys[name] = key
        self.secrets = list(self.keys.values())
        path = out / 'manifest.json'
        self.state = json.loads(path.read_text()) if path.exists() else {
            'id': run_id, 'manifest': manifest, 'requestsUsed': 0}
        if self.state['id'] != run_id:
            raise ValueError('Run configuration changed. Use a new output directory.')
        atomic_json(path, self.state, self.secrets)

    def save(self, task):
        atomic_json(self.out / (task['id'] + '.json'), task, self.secrets)

    def available(self):
        if self.stop.is_set() or time.monotonic() >= self.deadline:
            raise Pause('Run stopped or time limit reached; resume with the same command.')

    def wait(self, until):
        while time.time() < until:
            self.available()
            self.stop.wait(min(1, until - time.time()))

    def reserve(self):
        with self.mutex:
            self.available()
            if self.state['requestsUsed'] >= self.cap:
                raise Pause('Request cap reached; raise maxRequests explicitly to resume.')
            self.state['requestsUsed'] += 1
            atomic_json(self.out / 'manifest.json', self.state, self.secrets)

    def request(self, method, url, route, payload=None):
        name = route.get('keyEnv') or KEYS[route['provider']]
        headers = {'Authorization': 'Bearer ' + self.keys[name], 'Content-Type': 'application/json'}
        if route['provider'] == 'Google':
            headers = {'x-goog-api-key': self.keys[name], 'Content-Type': 'application/json'}
        request = urllib.request.Request(url, method=method, headers=headers,
                  data=json.dumps(payload).encode() if payload is not None else None)
        try:
            with urllib.request.urlopen(request, timeout=min(60, max(1, self.deadline - time.monotonic()))) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            retry_after = error.headers.get('Retry-After') if error.headers else None
            error.close()
            raise HTTPFailure(error.code, retry_after) from None
        except http.client.HTTPException:
            raise urllib.error.URLError('Provider connection failed.') from None

    def defer(self, task, error, attempts):
        delay = min(60, 5 * 2 ** (attempts - 1))
        if isinstance(error, HTTPFailure) and error.retry_after:
            try:
                delay = max(delay, float(error.retry_after))
            except ValueError:
                try:
                    delay = max(delay, parsedate_to_datetime(error.retry_after).timestamp() - time.time())
                except (ValueError, TypeError, OverflowError):
                    pass
        task['nextAttemptAt'] = time.time() + delay
        self.save(task)

    def get(self, task, route, path):
        self.wait(task.get('nextAttemptAt', 0))
        self.reserve()
        try:
            value = self.request('GET', BASE + path, route)
        except (HTTPFailure, urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            # Retry the same snapshot first, before failing this collection attempt.
            task['readFailures'] = task.get('readFailures', 0) + 1
            self.defer(task, error, min(task['readFailures'], 5))
            return None
        task['readFailures'] = 0
        task.pop('nextAttemptAt', None)
        self.save(task)
        return value

    def failed_attempt(self, task, attempt, reason):
        attempt.update(status='Error', error=reason)
        task['status'] = 'Pending'
        task['nextAttemptAt'] = max(task.get('nextAttemptAt', 0), time.time() + 5)
        self.save(task)

    def collect(self, task, route):
        from run import complete, payload_for as api_payload
        from extractors import extract_openai, extract_gemini, extract_perplexity
        if task['status'] in ('Submitting', 'FallbackSubmitting'):
            task.update(status='SubmissionUnknown', error='Interrupted submission; inspect provider history before starting another round.')
            self.save(task)
        while task['status'] not in TERMINAL:
            self.available()
            self.wait(task.get('nextAttemptAt', 0))
            attempts = task['brightDataAttempts']
            if attempts and attempts[-1]['status'] == 'Submitted':
                attempt = attempts[-1]
                expired = time.time() - attempt['submittedAt'] >= SNAPSHOT_TIMEOUT_SECONDS
                snapshot = urllib.parse.quote(attempt['snapshotId'], safe='')
                if not attempt.get('ready'):
                    progress = self.get(task, route, '/progress/' + snapshot)
                    if progress is None:
                        if expired:
                            raise Pause('Snapshot deadline reached but progress unavailable; resume to check the saved snapshot.')
                        continue
                    attempt['progress'] = progress
                    status = progress.get('status') if isinstance(progress, dict) else None
                    if status in WAITING:
                        if expired:
                            self.failed_attempt(task, attempt, 'Snapshot still unfinished after the 20 minute collection deadline.')
                            continue
                        task['nextAttemptAt'] = time.time() + self.poll_interval
                        self.save(task)
                        continue
                    if status in ('failed', 'error'):
                        self.failed_attempt(task, attempt, 'Snapshot failed.')
                        continue
                    if status != 'ready':
                        raise Pause('Unknown progress response; snapshot retained for inspection.')
                    attempt['ready'] = True
                    self.save(task)
                rows = self.get(task, route, '/snapshot/' + snapshot + '?format=json')
                if rows is None:
                    if expired:
                        raise Pause('Snapshot deadline reached but download unavailable; resume to check the saved snapshot.')
                    continue
                if isinstance(rows, dict) and rows.get('status') in WAITING:
                    if expired:
                        self.failed_attempt(task, attempt, 'Snapshot still building after the 20 minute collection deadline.')
                        continue
                    task['nextAttemptAt'] = time.time() + self.poll_interval
                    self.save(task)
                    continue
                attempt['raw'] = rows
                try:
                    if not isinstance(rows, list) or len(rows) != 1:
                        raise ValueError('Expected exactly one Bright Data record.')
                    if isinstance(rows[0], dict) and rows[0].get('prompt', task['prompt']['text']) != task['prompt']['text']:
                        raise ValueError('Bright Data returned a different prompt.')
                    text, cited, sources = extract_row(rows[0])
                except ValueError as error:
                    self.failed_attempt(task, attempt, str(error))
                    continue
                attempt['status'] = 'Captured'
                task.update(status='Captured', provider='BrightData', collection='Consumer UI',
                            answer=text, citations=cited, retrievedSources=sources, raw=rows[0],
                            model=rows[0]['model'] if isinstance(rows[0].get('model'), str) else '', searchEnabled=route.get('search'),
                            searchBackend='Bright Data consumer surface', region=route['country'])
                break
            if len(attempts) < BRIGHTDATA_ATTEMPTS:
                self.reserve()
                attempt = {'number': len(attempts) + 1, 'status': 'Submitting'}
                attempts.append(attempt)
                task['status'] = 'Submitting'
                self.save(task)
                try:
                    response = self.request('POST', BASE + '/trigger?' + urllib.parse.urlencode({
                        'dataset_id': route['datasetId'], 'include_errors': 'true', 'format': 'json'}),
                        route, payload_for(task['prompt']['text'], route))
                except HTTPFailure as error:
                    if 400 <= error.code < 500 and error.code != 408:
                        self.failed_attempt(task, attempt, str(error))
                        self.defer(task, error, len(attempts))
                        continue
                    task.update(status='SubmissionUnknown', error='Bright Data submission outcome unknown; inspect provider history.')
                    break
                except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                    task.update(status='SubmissionUnknown', error='Bright Data submission outcome unknown; inspect provider history.')
                    break
                snapshot = response.get('snapshot_id') if isinstance(response, dict) else None
                if not isinstance(snapshot, str) or not snapshot:
                    task.update(status='SubmissionUnknown', error='Submission returned no snapshot ID; inspect provider history.')
                    break
                attempt.update(status='Submitted', snapshotId=snapshot, submittedAt=time.time())
                task['status'] = 'Submitted'
                self.save(task)
                continue
            # Three unsuccessful Bright Data attempts; use the same surface's API.
            fallback = route['fallback']
            api_attempts = task.setdefault('apiAttempts', [])
            if len(api_attempts) >= API_ATTEMPTS:
                task.update(status='Error', error='API fallback exhausted after three attempts.')
                break
            self.reserve()
            task['fallbackUsed'] = True
            api_attempt = {'number': len(api_attempts) + 1, 'status': 'Submitting'}
            api_attempts.append(api_attempt)
            task['status'] = 'FallbackSubmitting'
            self.save(task)
            url, payload = api_payload(task['prompt']['text'], fallback)
            try:
                raw = self.request('POST', url, fallback, payload)
            except HTTPFailure as error:
                if 400 <= error.code < 500 and error.code != 408:
                    api_attempt.update(status='Error', error=str(error))
                    task['status'] = 'Pending'
                    self.defer(task, error, len(api_attempts))
                    continue
                task.update(status='SubmissionUnknown', error='API submission outcome unknown; inspect provider history.')
                break
            except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                task.update(status='SubmissionUnknown', error='API submission outcome unknown; inspect provider history.')
                break
            extractor = {'OpenAI': extract_openai, 'Google': extract_gemini, 'Perplexity': extract_perplexity}[fallback['provider']]
            try:
                if not isinstance(raw, dict):
                    raise ValueError('Expected an API response object.')
                text, cited, sources, *searched = extractor(raw)
                succeeded = complete(raw, fallback, text)
            except (ValueError, TypeError, AttributeError, KeyError):
                succeeded = False
                api_attempt['error'] = 'API response could not be parsed.'
            api_attempt.update(status='Captured' if succeeded else 'Incomplete', raw=raw)
            if not succeeded:
                task['status'] = 'Pending'
                task['nextAttemptAt'] = time.time() + 5
                self.save(task)
                continue
            task.update(status='Captured', provider=fallback['provider'], collection='API',
                        requestedModel=fallback['model'], model=raw.get('model', raw.get('modelVersion', fallback['model'])),
                        answer=text, citations=cited, retrievedSources=sources, raw=raw,
                        searchEnabled=fallback['search'], searchBackend=fallback['searchBackend'],
                        region='', searchPerformed=searched[0] if searched else None)
        if task['status'] in TERMINAL:
            task['completedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            self.save(task)

    def work(self, prompt, route, repetition):
        from run import digest, now
        identity = digest({'run': self.run_id, 'prompt': prompt, 'route': route, 'repetition': repetition})[:24]
        path = self.out / (identity + '.json')
        task = json.loads(path.read_text()) if path.exists() else {
            'id': identity, 'runId': self.run_id, 'prompt': prompt, 'engine': route['label'],
            'provider': 'BrightData', 'collection': 'Consumer UI', 'repetition': repetition,
            'requestedAt': now(), 'status': 'Pending', 'brightDataAttempts': []}
        if task['status'] not in TERMINAL:
            self.save(task)
            try:
                self.collect(task, route)
                task.pop('pauseReason', None)
            except Pause as error:
                task['pauseReason'] = str(error)
            self.save(task)
        print(f"{route['label']} {prompt['id']} repetition {repetition}: {task['status']}"
              + (' (API fallback)' if task.get('fallbackUsed') else ''), flush=True)
        return task['status']


def run_cohort(args, config, manifest, run_id):
    from run import env_file
    count = len(manifest['prompts']) * len(manifest['providers']) * manifest['repetitions']
    print(f'{count} results; {MAX_CONCURRENT_TASKS} workers; up to 3 Bright Data attempts then API fallback; run {run_id}.')
    if args.dry_run:
        # Validate operational settings too, without reading keys or writing files.
        for name, default in [('maxRequests', 1000), ('pollIntervalSeconds', 15), ('maxRunSeconds', 3600)]:
            if type(config.get(name, default)) is not int or config.get(name, default) < 1:
                raise ValueError(name + ' must be a positive integer')
        return 0
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with output_lock(out):
        runner = Runner(out, manifest, run_id, config, env_file(args.env))
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS) as pool:
            futures = [pool.submit(runner.work, prompt, route, repetition)
                       for prompt in manifest['prompts'] for route in manifest['providers']
                       for repetition in range(1, manifest['repetitions'] + 1)]
            try:
                statuses = [future.result() for future in as_completed(futures)]
            finally:
                runner.stop.set()
        print(f"Captured {statuses.count('Captured')}/{count}; HTTP requests {runner.state['requestsUsed']}/{runner.cap}. "
              'Pending tasks resume with the same command. SubmissionUnknown needs provider-history review.')
        return 0 if all(s == 'Captured' for s in statuses) else 1
