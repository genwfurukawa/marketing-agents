import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {metrics,toCSV,parseCSV,safeURL} from '../src/lib/core.mjs';
import {workspaceStore} from '../src/storage.mjs';
test('reviewed discovery denominator excludes branded, failed and unreviewed records',()=>{
 const prompts=[{id:'d',group:'Discovery'},{id:'c',group:'Comparison'}];
 const answers=[{promptId:'d',status:'Captured',recommended:true,mentioned:true,assessmentReviewed:true},{promptId:'d',status:'Captured',recommended:false,assessmentReviewed:false},{promptId:'c',status:'Captured',recommended:true},{promptId:'d',status:'Error',recommended:false}];
 assert.equal(metrics(answers,prompts).recommendation,100);assert.equal(metrics(answers,prompts).discovery,1);assert.equal(metrics(answers,prompts).captured,3);
});
test('retrieved sources never count as final citations; unchecked accuracy is unknown',()=>{
 const m=metrics([{status:'Captured',retrievedSources:[{url:'https://demo.example'}]}],[]);assert.equal(m.citation,0);assert.equal(m.accuracy,null);
});
test('CSV multiline and formula protection; URLs reject executable schemes',()=>{
 const rows=[{text:'hello, "world"\nnext',notes:'=HYPERLINK("bad")'}];const restored=parseCSV(toCSV(rows));assert.equal(restored[0].text,rows[0].text);assert.ok(restored[0].notes.startsWith("'="));assert.equal(safeURL('javascript:alert(1)'),null);
});
test('SQLite survives reopening and rejects stale writes',()=>{
 const dir=mkdtempSync(join(tmpdir(),'prompt-tracker-'));const path=join(dir,'test.sqlite');const seed={projects:[],prompts:[],answers:[],content:[],experiments:[]};
 const a=workspaceStore(path,seed);assert.equal(a.read().version,0);assert.equal(a.save({...seed,marker:'saved'},0),1);assert.equal(a.save(seed,0),null);a.close();
 const b=workspaceStore(path,seed);assert.equal(b.read().data.marker,'saved');assert.equal(b.read().version,1);b.close();rmSync(dir,{recursive:true,force:true});
});
