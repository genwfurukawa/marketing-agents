import {DatabaseSync} from 'node:sqlite';
import {mkdirSync} from 'node:fs';
import {dirname} from 'node:path';
export function workspaceStore(path,seed){
 mkdirSync(dirname(path),{recursive:true});const db=new DatabaseSync(path);
 db.exec('CREATE TABLE IF NOT EXISTS workspace (id INTEGER PRIMARY KEY CHECK(id=1),data TEXT NOT NULL,version INTEGER NOT NULL)');
 return {read(){const row=db.prepare('SELECT data,version FROM workspace WHERE id=1').get();return row?{data:JSON.parse(row.data),version:row.version}:{data:structuredClone(seed),version:0};},
 save(data,version){db.exec('BEGIN IMMEDIATE');try{const current=db.prepare('SELECT version FROM workspace WHERE id=1').get();if((current?.version??0)!==version){db.exec('ROLLBACK');return null;}const next=version+1;db.prepare('INSERT INTO workspace(id,data,version) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data,version=excluded.version').run(JSON.stringify(data),next);db.exec('COMMIT');return next;}catch(e){db.exec('ROLLBACK');throw e;}},close(){db.close();}};
}
