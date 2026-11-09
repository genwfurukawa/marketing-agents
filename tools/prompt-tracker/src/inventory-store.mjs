import {DatabaseSync} from 'node:sqlite';
import {mkdirSync} from 'node:fs';
import {dirname} from 'node:path';
import {randomUUID} from 'node:crypto';
export {domainHost} from './lib/source-ownership.mjs';
import {domainHost} from './lib/source-ownership.mjs';

export const EMBEDDING_MODEL = 'text-embedding-3-small';
export const EMBEDDING_DIMENSIONS = 1536;

export function pageURL(value) {
  const url = new URL(value);
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) throw Error('Invalid page URL.');
  url.hash = '';
  url.hostname = url.hostname.toLowerCase().replace(/^www\./, '');
  for (const key of [...url.searchParams.keys()]) if (/^utm_/i.test(key)) url.searchParams.delete(key);
  url.searchParams.sort();
  return url.href;
}

export function citationCounts(answers) {
  const counts = new Map();
  for (const answer of answers.filter(a => a.status === 'Captured')) {
    const urls = new Set();
    for (const field of ['ownedCitations', 'thirdPartyCitations']) {
      for (const url of String(answer[field] || '').split(/[,\n]/).map(s => s.trim()).filter(Boolean)) {
        try { urls.add(pageURL(url)); } catch { /* Invalid capture URLs do not become sources. */ }
      }
    }
    for (const url of urls) counts.set(url, (counts.get(url) || 0) + 1);
  }
  return counts;
}

export function inventoryStore(path) {
  mkdirSync(dirname(path), {recursive: true});
  const db = new DatabaseSync(path);
  db.exec(`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS domains (
      id TEXT PRIMARY KEY, project_id TEXT NOT NULL, host TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Idle', last_attempt TEXT, last_success TEXT,
      error TEXT NOT NULL DEFAULT '', run_token TEXT, lease_until INTEGER,
      UNIQUE(project_id,host)
    );
    CREATE TABLE IF NOT EXISTS pages (
      id INTEGER PRIMARY KEY, domain_id TEXT NOT NULL REFERENCES domains(id), url TEXT NOT NULL,
      title TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '',
      content TEXT NOT NULL DEFAULT '', content_hash TEXT NOT NULL DEFAULT '',
      fetched_at TEXT, checked_at TEXT, fetch_status TEXT NOT NULL DEFAULT 'Pending',
      error TEXT NOT NULL DEFAULT '', http_status INTEGER, canonical TEXT NOT NULL DEFAULT '',
      robots TEXT NOT NULL DEFAULT '', indexed_hash TEXT, embedding_model TEXT,
      indexed_at TEXT, index_error TEXT NOT NULL DEFAULT '', embedding BLOB, UNIQUE(domain_id,url)
    );
    CREATE INDEX IF NOT EXISTS pages_domain ON pages(domain_id);`);
  const transaction = fn => { db.exec('BEGIN IMMEDIATE'); try { const result = fn(); db.exec('COMMIT'); return result; } catch (e) { db.exec('ROLLBACK'); throw e; } };
  const owns = (id, token) => { if (!db.prepare('SELECT 1 FROM domains WHERE id=? AND run_token=?').get(id, token)) throw Error('Refresh ownership lost.'); };
  return {
    add(projectId, value) {
      const host = domainHost(value);
      db.prepare('INSERT INTO domains(id,project_id,host) VALUES(?,?,?) ON CONFLICT(project_id,host) DO NOTHING').run(randomUUID(), projectId, host);
      return db.prepare('SELECT * FROM domains WHERE project_id=? AND host=?').get(projectId, host);
    },
    domain(id) { return db.prepare('SELECT * FROM domains WHERE id=?').get(id); },
    list(projectId) {
      return db.prepare(`SELECT d.id,d.host,d.status,d.last_attempt,d.last_success,d.error,d.lease_until,
        COUNT(p.id) page_count, SUM(CASE WHEN p.indexed_hash=p.content_hash AND p.indexed_hash IS NOT NULL THEN 1 ELSE 0 END) indexed_count
        FROM domains d LEFT JOIN pages p ON p.domain_id=d.id WHERE d.project_id=? GROUP BY d.id ORDER BY d.host`).all(projectId).map(row=>({...row,status:row.status==='Running'&&row.lease_until<Date.now()?'Interrupted':row.status}));
    },
    pages(domainId) { return db.prepare(`SELECT id,url,title,description,fetched_at,checked_at,fetch_status,error,http_status,
      indexed_at,index_error,embedding_model,(indexed_hash=content_hash AND indexed_hash IS NOT NULL) AS "indexed"
      FROM pages WHERE domain_id=? ORDER BY url`).all(domainId); },
    page(id) { return db.prepare('SELECT p.*,d.project_id FROM pages p JOIN domains d ON d.id=p.domain_id WHERE p.id=?').get(id); },
    pageByURL(domainId, url) { return db.prepare('SELECT * FROM pages WHERE domain_id=? AND url=?').get(domainId, pageURL(url)); },
    begin(id) {
      return transaction(() => {
        const domain = db.prepare('SELECT * FROM domains WHERE id=?').get(id);
        if (!domain) throw Error('Unknown domain.');
        if (domain.run_token && domain.lease_until > Date.now()) throw Error('A refresh is already running.');
        const token = randomUUID();
        db.prepare("UPDATE domains SET status='Running',last_attempt=?,error='',run_token=?,lease_until=? WHERE id=?")
          .run(new Date().toISOString(), token, Date.now() + 120000, id);
        return token;
      });
    },
    heartbeat(id, token) { owns(id, token); db.prepare('UPDATE domains SET lease_until=? WHERE id=? AND run_token=?').run(Date.now() + 120000, id, token); },
    savePage(domainId, token, page) {
      return transaction(() => {
        owns(domainId, token);
        const url = pageURL(page.url);
        const previous = db.prepare('SELECT * FROM pages WHERE domain_id=? AND url=?').get(domainId, url);
        if (previous && previous.content_hash !== page.hash) {
          db.prepare('UPDATE pages SET indexed_hash=NULL,embedding_model=NULL,indexed_at=NULL,embedding=NULL WHERE id=?').run(BigInt(previous.id));
        }
        db.prepare(`INSERT INTO pages(domain_id,url,title,description,content,content_hash,fetched_at,checked_at,fetch_status,http_status,canonical,robots)
          VALUES(?,?,?,?,?,?,?,?, 'Fetched',?,?,?) ON CONFLICT(domain_id,url) DO UPDATE SET
          title=excluded.title,description=excluded.description,content=excluded.content,content_hash=excluded.content_hash,
          fetched_at=excluded.fetched_at,checked_at=excluded.checked_at,fetch_status='Fetched',error='',
          http_status=excluded.http_status,canonical=excluded.canonical,robots=excluded.robots`).run(
            domainId, url, page.title, page.description, page.content, page.hash, new Date().toISOString(), new Date().toISOString(), page.status, page.canonical, page.robots);
        return db.prepare('SELECT * FROM pages WHERE domain_id=? AND url=?').get(domainId, url);
      });
    },
    failPage(domainId, token, url, error, status=null) {
      transaction(() => { owns(domainId, token); db.prepare(`INSERT INTO pages(domain_id,url,checked_at,fetch_status,error,http_status)
        VALUES(?,?,?,'Failed',?,?) ON CONFLICT(domain_id,url) DO UPDATE SET
        checked_at=excluded.checked_at,fetch_status='Failed',error=excluded.error,http_status=excluded.http_status`)
        .run(domainId, pageURL(url), new Date().toISOString(), error, status); });
    },
    index(pageId, token, hash, vector) {
      if (!Array.isArray(vector) || vector.length !== EMBEDDING_DIMENSIONS || !vector.every(Number.isFinite)) throw Error('Invalid embedding vector.');
      const packed=new Float32Array(vector);
      if(!packed.every(Number.isFinite)||!packed.some(v=>v!==0))throw Error('Invalid embedding vector.');
      transaction(() => {
        const page = db.prepare('SELECT * FROM pages WHERE id=?').get(pageId);
        owns(page.domain_id, token);
        if (page.content_hash !== hash) throw Error('Page changed while indexing.');
        const bytes=Buffer.alloc(EMBEDDING_DIMENSIONS*4);
        packed.forEach((value,i)=>bytes.writeFloatLE(value,i*4));
        db.prepare("UPDATE pages SET embedding=?,indexed_hash=?,embedding_model=?,indexed_at=?,index_error='' WHERE id=?")
          .run(bytes, hash, EMBEDDING_MODEL, new Date().toISOString(), pageId);
      });
    },
    indexFailed(pageId, token, message) {
      transaction(() => { const page = db.prepare('SELECT domain_id FROM pages WHERE id=?').get(pageId); owns(page.domain_id, token);
        db.prepare('UPDATE pages SET index_error=? WHERE id=?').run(message, pageId); });
    },
    finish(id, token, status, message='') {
      transaction(() => { owns(id, token); db.prepare(`UPDATE domains SET status=?,error=?,run_token=NULL,lease_until=NULL,
        last_success=CASE WHEN ?='Complete' THEN ? ELSE last_success END WHERE id=?`).run(status, message, status, new Date().toISOString(), id); });
    },
    close() { db.close(); },
  };
}
