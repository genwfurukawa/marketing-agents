import React,{useEffect,useState} from 'react';
import {comparisonMetrics,currentSuggestion,H2H_OUTCOMES} from './lib/head-to-head.mjs';
type Item=Record<string,any>;
const label=(value:string)=>({we_win:'Client wins',competitor_wins:'Competitor wins',tie:'Tie',not_compared:'Not compared'}[value]||'Unscored');

export function ComparisonSummary({answers,prompts}:{answers:Item[];prompts:Item[]}) {
 const stats=comparisonMetrics(answers,prompts);
 return <article className='panel settings-panel'><h2>Head-to-head comparisons</h2><p>Reviewed Comparison answers only. Win rate = wins ÷ (wins + losses + ties). Not-compared and unreviewed answers are excluded.</p>
  <div className='summary-strip'><span><b>{stats.winRate===null?'—':stats.winRate+'%'}</b> win rate</span><span><b>{stats.wins}</b> wins</span><span><b>{stats.losses}</b> losses</span><span><b>{stats.ties}</b> ties</span><span><b>{stats.notCompared}</b> not compared</span></div>
  {stats.mixedRoutes&&<p className='method-note'>This view mixes collection routes or models. Use the existing surface and collection filters before comparing results.</p>}
  <p className='method-note'>Keep prompt versions and collection conditions consistent when comparing weeks. These rates use reviewed answers, not every collected answer.</p>
  {stats.competitors.length?<div className='table-wrap'><table><thead><tr><th>Competitor</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Win rate</th></tr></thead><tbody>{stats.competitors.map(row=><tr key={row.name}><td>{row.name}</td><td>{row.wins}</td><td>{row.losses}</td><td>{row.ties}</td><td>{row.winRate===null?'—':row.winRate+'%'}</td></tr>)}</tbody></table></div>:<p>Score or manually label Comparison answers, then confirm review to start tracking wins.</p>}
  {!!stats.weeks.length&&<><h3>Weekly results (UTC)</h3><div className='table-wrap'><table><thead><tr><th>Week starting</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Win rate</th></tr></thead><tbody>{stats.weeks.map(row=><tr key={row.week}><td>{row.week}</td><td>{row.wins}</td><td>{row.losses}</td><td>{row.ties}</td><td>{row.winRate===null?'—':row.winRate+'%'}</td></tr>)}</tbody></table></div></>}
 </article>;
}

export function ComparisonReview({answer,prompt,project,onSave}:{answer:Item;prompt:Item;project:Item;onSave:(answer:Item)=>Promise<boolean>}) {
 const [outcome,setOutcome]=useState(answer.h2hOutcome||''),[competitor,setCompetitor]=useState(answer.h2hCompetitor||project.competitors[0]||'');
 const [valid,setValid]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState('');
 const suggestion=answer.scoringSuggestion;
 useEffect(()=>{let active=true;setValid(false);currentSuggestion(answer,prompt,project).then(value=>{if(active)setValid(value);}).catch(()=>{});return()=>{active=false;};},[answer,prompt,project]);
 async function persist(next:Item){setBusy(true);setError('');try{if(!await onSave(next))setError('Could not save comparison labels. Refresh the dashboard if another process changed the workspace.');}catch{setError('Could not save comparison labels.');}finally{setBusy(false);}}
 async function useSuggestion(){if(!await currentSuggestion(answer,prompt,project)){setError('Suggestion no longer matches this answer or project. Rescore it.');return;}
  const brands=(suggestion.recommendedCompany?[suggestion.recommendedCompany]:[]).join(', ');
  setOutcome(suggestion.outcome);setCompetitor(suggestion.competitor);
  await persist({...answer,h2hOutcome:suggestion.outcome,h2hCompetitor:suggestion.competitor,h2hSubjectAssessment:suggestion.subjectAssessment,h2hCompetitorAssessment:suggestion.competitorAssessment,
   h2hEvidence:suggestion.evidence,mentioned:suggestion.mentioned,recommended:suggestion.recommended,brands,assessmentReviewed:false});
 }
 return <section className='panel settings-panel'><h3>Head-to-head labels</h3>
  <p>Applying or changing labels resets review. Use Edit capture to confirm review afterward.</p>
  {!!suggestion&&<><h4>Scorer suggestion</h4>{valid?<><p><b>{label(suggestion.outcome)}</b> against {suggestion.competitor}</p><p>Overall recommendation: {suggestion.recommendedCompany||'No single unconditional pick'}</p>
   <p>{suggestion.subjectAssessment}</p><p>{suggestion.competitorAssessment}</p>
   {Object.entries(suggestion.evidence).map(([key,value]:[string,any])=>value&&<blockquote key={key}>{value.text}</blockquote>)}
   <small>Scored {new Date(suggestion.scoredAt).toLocaleString()} · Jev: {suggestion.models.jev} · OpenAI: {suggestion.models.openaiReturned}</small>
   <p><button className='button primary' disabled={busy} onClick={useSuggestion}>Use suggested labels</button></p></>:<p>Suggestion is stale or unverified. Rescore this answer before applying it.</p>}</>}
  <form className='inventory-form' onSubmit={async event=>{event.preventDefault();await persist({...answer,h2hOutcome:outcome||undefined,h2hCompetitor:outcome?competitor:undefined,h2hEvidence:undefined,h2hSubjectAssessment:undefined,h2hCompetitorAssessment:undefined,assessmentReviewed:false});}}>
   <label>Competitor<select aria-label='Head-to-head competitor' value={competitor} onChange={e=>setCompetitor(e.target.value)}>{project.competitors.map((name:string)=><option key={name}>{name}</option>)}</select></label>
   <label>Outcome<select aria-label='Head-to-head outcome' value={outcome} onChange={e=>setOutcome(e.target.value)}><option value=''>Unscored</option>{H2H_OUTCOMES.map(value=><option key={value} value={value}>{label(value)}</option>)}</select></label>
   <button className='button ghost' disabled={busy||(!competitor&&!!outcome)}>Save comparison labels</button>
  </form>{error&&<p role='alert'>{error}</p>}
 </section>;
}
