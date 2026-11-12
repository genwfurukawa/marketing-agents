#!/usr/bin/env python3
"""Score saved Comparison answers, then attach reviewable suggestions locally."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import http.client
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import urllib.error
import urllib.request

from brightdata import atomic_json, output_lock, MAX_CONCURRENT_TASKS
from run import digest, env_file, now
from head_to_head import VERSION, JEV_MODEL, context_for, decision_request, parse_decisions, writer_payload, parse_writer, checked_score

DEFAULT_DB = Path(__file__).resolve().parents[1] / '.data/workspace.sqlite'


def text_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def read_workspace(path):
    if not Path(path).is_file():
        raise ValueError('Open the dashboard and import captured answers before scoring.')
    with closing(sqlite3.connect(path)) as db:
        row = db.execute('SELECT data FROM workspace WHERE id=1').fetchone()
    if not row:
        raise ValueError('No saved workspace exists yet.')
    return json.loads(row[0])


def apply_suggestions(path, project_id, artifacts):
    """Short transaction after provider work; never update manually scored fields."""
    with closing(sqlite3.connect(path, timeout=5)) as db, db:
        db.execute('BEGIN IMMEDIATE')
        row = db.execute('SELECT data,version FROM workspace WHERE id=1').fetchone()
        workspace = json.loads(row[0])
        project = next((p for p in workspace['projects'] if p['id'] == project_id), None)
        if not project:
            raise ValueError('Client project was removed while scoring.')
        answers = {a['id']: a for a in workspace['answers'] if a['projectId'] == project_id}
        prompts = {p['id']: p for p in workspace['prompts'] if p['projectId'] == project_id}
        applied = skipped = 0
        for artifact in artifacts:
            if artifact['status'] != 'Scored':
                continue
            answer = answers.get(artifact['answerId'])
            prompt = prompts.get(answer['promptId']) if answer else None
            if not answer or not prompt:
                skipped += 1
                continue
            try:
                context = context_for(project, prompt, answer, artifact['pair'])
            except ValueError:
                skipped += 1
                continue
            if digest(context) != artifact['contextHash']:
                skipped += 1
                continue
            if (answer.get('scoringSuggestion') or {}).get('artifactId') == artifact['id']:
                continue
            # Manual labels and review status stay untouched, even on rescoring.
            answer['scoringSuggestion'] = {
                **artifact['score'], 'version': VERSION, 'textHash': text_hash(answer['text']),
                'promptVersion': prompt['version'], 'promptText': prompt['text'],
                'subject': project['name'], 'pair': artifact['pair'],
                'scoredAt': artifact['completedAt'], 'models': artifact['models'],
                'artifactId': artifact['id'],
            }
            applied += 1
        if applied:
            serialized=json.dumps(workspace,ensure_ascii=False,separators=(',',':'))
            if len(serialized.encode())>8_000_000:
                raise ValueError('Suggestions would exceed the dashboard workspace size limit; no changes were saved.')
            db.execute('UPDATE workspace SET data=?,version=? WHERE id=1', (serialized, row[1] + 1))
        return applied, skipped


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post(url, payload, key):
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
        'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=90) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        error.close()
        raise ValueError(f'Scoring provider HTTP {error.code}; inspect the saved task before retrying.') from None
    except (OSError, ValueError, http.client.HTTPException):
        raise ValueError('Scoring connection or response failed; submission may have been billed.') from None


class Scorer:
    def __init__(self, output, config, env, run_id):
        self.output, self.config, self.run_id = output, config, run_id
        self.keys = {name: env.get(name, '').strip() for name in ('TYPESAFE_API_KEY', 'OPENAI_API_KEY')}
        for name, key in self.keys.items():
            if not key or not key.isascii() or any(c.isspace() or not c.isprintable() for c in key):
                raise ValueError('Missing or invalid ' + name)
        self.secrets = list(self.keys.values())
        self.lock = threading.Lock()
        self.stop = threading.Event()
        path = output / 'manifest.json'
        self.state = json.loads(path.read_text()) if path.exists() else {'id': run_id, 'requestsUsed': 0, 'createdAt': now()}
        if self.state['id'] != run_id:
            raise ValueError('Scoring inputs or models changed. Use a new output folder.')
        atomic_json(path, self.state, self.secrets)

    def save(self, task):
        atomic_json(self.output / (task['id'] + '.json'), task, self.secrets)

    def reserve(self):
        with self.lock:
            if self.stop.is_set() or self.state['requestsUsed'] >= self.config['maxRequests']:
                return False
            self.state['requestsUsed'] += 1
            atomic_json(self.output / 'manifest.json', self.state, self.secrets)
            return True

    def work(self, job):
        identity = digest({'run': self.run_id, 'answerId': job['answerId'], 'context': job['context']})[:24]
        path = self.output / (identity + '.json')
        task = json.loads(path.read_text()) if path.exists() else {
            'id': identity, 'answerId': job['answerId'], 'projectId': job['projectId'], 'pair': job['pair'],
            'contextHash': digest(job['context']), 'status': 'Pending', 'version': VERSION,
            'models': {'jev': self.config['jevModel'], 'openaiRequested': self.config['openaiModel']}}
        if task['status'] in ('Scored', 'Hold', 'SubmissionUnknown'):
            return task
        if task['status'] in ('JevSubmitting', 'OpenAISubmitting'):
            task.update(status='SubmissionUnknown', error='Interrupted submission; inspect provider history before repeating a paid call.')
            self.save(task)
            return task
        try:
            if task['status'] == 'Pending':
                if not self.reserve():
                    self.save(task)
                    return task
                request = decision_request(job['context'])
                request['model'] = self.config['jevModel']
                task['status'] = 'JevSubmitting'
                self.save(task)
                raw = post('https://api.typesafe.ai/v1/systemone', request, self.keys['TYPESAFE_API_KEY'])
                task['jevRaw'] = raw
                task['decisions'] = parse_decisions(request, raw)
                task['status'] = 'JevDone'
                self.save(task)
            if not self.reserve():
                return task
            task['status'] = 'OpenAISubmitting'
            self.save(task)
            raw = post('https://api.openai.com/v1/responses', writer_payload(job['context'], task['decisions'], self.config['openaiModel']), self.keys['OPENAI_API_KEY'])
            task['openaiRaw'] = raw
            task['models']['openaiReturned'] = raw.get('model')
            task['score'] = checked_score(job['context'], task['decisions'], parse_writer(raw))
            task.update(status='Scored', completedAt=now())
        except ValueError as error:
            task.update(status='Hold',error=str(error))
        except (TypeError, KeyError, AttributeError):
            # Unexpected response shapes get a sanitized message; don't print provider content.
            task.update(status='Hold', error='Provider output or evidence could not be validated; review raw task/provider history. No labels were applied.')
        self.save(task)
        return task


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True); parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True); parser.add_argument('--env')
    parser.add_argument('--database', default=str(DEFAULT_DB)); parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    if not isinstance(config,dict) or not isinstance(config.get('comparisons',{}),dict):
        raise ValueError('Scorer configuration and comparisons must be JSON objects.')
    config.setdefault('jevModel', JEV_MODEL); config.setdefault('maxRequests', 50)
    if not isinstance(config.get('openaiModel'), str) or not config['openaiModel'].strip() or config['openaiModel'].startswith('REPLACE_'):
        raise ValueError('Configure an available exact OpenAI scoring model.')
    if not isinstance(config['jevModel'], str) or not config['jevModel'].startswith('jev-') or 'latest' in config['jevModel']:
        raise ValueError('Configure a pinned Jev model, not a moving latest alias.')
    if type(config['maxRequests']) is not int or config['maxRequests'] < 1:
        raise ValueError('maxRequests must be a positive integer.')
    workspace = read_workspace(args.database)
    project = next((p for p in workspace['projects'] if p['id'] == args.project), None)
    if not project:
        raise ValueError('Unknown client project.')
    prompts = {p['id']: p for p in workspace['prompts'] if p['projectId'] == args.project}
    jobs = []
    for answer in workspace['answers']:
        prompt = prompts.get(answer['promptId']) if answer['projectId'] == args.project else None
        if not prompt or prompt['group'] != 'Comparison' or answer['status'] != 'Captured':
            continue
        pair = config.get('comparisons', {}).get(prompt['id'], {})
        context = context_for(project, prompt, answer, pair)
        decision_request(context)  # Preflight the entire cohort before spending.
        jobs.append({'answerId': answer['id'], 'projectId': args.project, 'pair': pair, 'context': context})
    print(f'{len(jobs)} Comparison answers; at most {config["maxRequests"]} paid HTTP requests; five workers. No automatic retries.')
    if args.dry_run or not jobs:
        return
    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    identity = digest({'version': VERSION, 'jobs': jobs, 'jevModel': config['jevModel'], 'openaiModel': config['openaiModel']})[:24]
    with output_lock(output):
        scorer = Scorer(output, config, env_file(args.env), identity)
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS) as pool:
            try:
                artifacts = list(pool.map(scorer.work, jobs))
            finally:
                scorer.stop.set()
        applied, skipped = apply_suggestions(args.database, args.project, artifacts)
    print(f'Saved {applied} suggestions; {skipped} changed inputs skipped. Refresh the dashboard and review suggestions in Answer evidence.')
    print('Task status: '+', '.join(f'{status}={sum(a["status"]==status for a in artifacts)}' for status in ('Scored','Hold','SubmissionUnknown','Pending','JevDone')))
    if any(a['status'] != 'Scored' for a in artifacts) or skipped:
        raise SystemExit(1)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, sqlite3.Error) as error:
        raise SystemExit(str(error)) from None
