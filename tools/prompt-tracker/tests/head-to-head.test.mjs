import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {comparisonMetrics,currentSuggestion} from '../src/lib/head-to-head.mjs';

test('head-to-head denominator includes ties and excludes unreviewed, missing, discovery and not-compared',()=>{
 const prompts=[{id:'c',group:'Comparison'},{id:'d',group:'Discovery'}];
 const row={promptId:'c',status:'Captured',assessmentReviewed:true,h2hCompetitor:'Rival',date:'2026-11-09',engine:'ChatGPT'};
 const stats=comparisonMetrics(['we_win','competitor_wins','tie','not_compared'].map(h2hOutcome=>({...row,h2hOutcome})).concat([
  {...row,h2hOutcome:'we_win',assessmentReviewed:false},{...row,h2hOutcome:'we_win',status:'Error'},
  {...row,h2hOutcome:'we_win',promptId:'d'},{...row,h2hOutcome:undefined}] ),prompts);
 assert.equal(stats.winRate,33);assert.equal(stats.decided,3);assert.equal(stats.notCompared,1);assert.equal(stats.competitors[0].wins,1);
 assert.equal(comparisonMetrics([{...row,h2hOutcome:'not_compared'}],prompts).winRate,null);
});

test('weeks normalize offset timestamps to UTC rather than the local calendar',()=>{
 const base={promptId:'c',status:'Captured',assessmentReviewed:true,h2hCompetitor:'Rival',h2hOutcome:'we_win'};
 const stats=comparisonMetrics([{...base,date:'2026-11-09T00:30:00+02:00'},{...base,date:'2026-11-09T00:30:00Z'}],[{id:'c',group:'Comparison'}]);
 assert.deepEqual(stats.weeks.map(w=>w.week),['2026-11-02','2026-11-09']);
});

test('suggestions are stale after answer edits, prompt changes or competitor removal',async()=>{
 const project={name:'Client',competitors:['Rival']},prompt={version:1,text:'Compare?'},text='An answer';
 const answer={text,scoringSuggestion:{version:'head-to-head-v1',subject:'Client',competitor:'Rival',promptVersion:1,promptText:'Compare?',textHash:createHash('sha256').update(text).digest('hex')}};
 assert.equal(await currentSuggestion(answer,prompt,project),true);
 assert.equal(await currentSuggestion({...answer,text:'Changed'},prompt,project),false);
 assert.equal(await currentSuggestion(answer,{...prompt,version:2},project),false);
 assert.equal(await currentSuggestion(answer,prompt,{...project,competitors:[]}),false);
});
