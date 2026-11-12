export const H2H_OUTCOMES=['we_win','competitor_wins','tie','not_compared'];

export function comparisonMetrics(answers,prompts) {
 const groups=new Map(prompts.map(p=>[p.id,p.group]));
 const eligible=answers.filter(a=>a.status==='Captured'&&a.assessmentReviewed===true&&groups.get(a.promptId)==='Comparison'&&H2H_OUTCOMES.includes(a.h2hOutcome)&&a.h2hCompetitor);
 const tally=rows=>{const wins=rows.filter(a=>a.h2hOutcome==='we_win').length,losses=rows.filter(a=>a.h2hOutcome==='competitor_wins').length,ties=rows.filter(a=>a.h2hOutcome==='tie').length;
  const decided=wins+losses+ties;return {wins,losses,ties,decided,notCompared:rows.length-decided,winRate:decided?Math.round(wins/decided*100):null};};
 const weekOf=value=>{const date=new Date(value);if(Number.isNaN(+date))return null;return new Date(Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate()-(date.getUTCDay()+6)%7)).toISOString().slice(0,10);};
 const weeks=[...new Set(eligible.map(a=>weekOf(a.date)).filter(Boolean))].sort();
 const routes=new Set(eligible.map(a=>JSON.stringify([a.engine,a.collection||'Consumer UI',a.provider||'',a.model||'',a.search||'Unknown'])));
 return {...tally(eligible),mixedRoutes:routes.size>1,
  competitors:[...new Set(eligible.map(a=>a.h2hCompetitor))].map(name=>({name,...tally(eligible.filter(a=>a.h2hCompetitor===name))})),
  weeks:weeks.map(week=>({week,...tally(eligible.filter(a=>weekOf(a.date)===week))}))};
}

export async function currentSuggestion(answer,prompt,project) {
 const suggestion=answer.scoringSuggestion;
 if(!suggestion||suggestion.version!=='head-to-head-v1'||suggestion.subject!==project.name||suggestion.promptVersion!==prompt.version||suggestion.promptText!==prompt.text||!project.competitors.includes(suggestion.competitor))return false;
 const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(answer.text));
 return suggestion.textHash===[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
