export const ENGINES = ['ChatGPT', 'Gemini', 'Claude', 'Perplexity', 'Google AI Overviews'];
export const list = value => String(value || '').split(/[,\n]/).map(s => s.trim()).filter(Boolean);
export function metrics(answers, prompts) {
  const groups = new Map(prompts.map(p => [p.id, p.group]));
  const captured = answers.filter(a => a.status === 'Captured');
  const discovery = captured.filter(a => a.assessmentReviewed !== false && groups.get(a.promptId) === 'Discovery');
  const totals = captured.reduce((m,a) => ({ checked:m.checked + Number(a.checkedClaims || 0), errors:m.errors + Number(a.errorClaims || 0) }), {checked:0,errors:0});
  const rate = (rows, test) => rows.length ? Math.round(rows.filter(test).length / rows.length * 100) : null;
  const searches = answers.filter(a => a.engine === 'Google AI Overviews' && ['Captured','No overview'].includes(a.status));
  return {captured:captured.length, discovery:discovery.length, mention:rate(discovery,a=>a.mentioned), recommendation:rate(discovery,a=>a.recommended), citation:rate(captured,a=>list(a.ownedCitations).length>0), accuracy:totals.checked ? Math.round((totals.checked-totals.errors)/totals.checked*100):null, checked:totals.checked, overview:rate(searches,a=>a.status==='Captured')};
}
export function parseCSV(text) {
  const rows=[]; let row=[], field='', quoted=false;
  text=text.replace(/^\uFEFF/,'');
  for(let i=0;i<text.length;i++) {const c=text[i]; if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted;} else if(c===','&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field='';}else field+=c;}
  if(quoted)throw new Error('CSV contains an unclosed quote.');
  row.push(field);if(row.some(Boolean))rows.push(row);
  const header=rows.shift()||[];
  return rows.map(r=>Object.fromEntries(header.map((h,i)=>[h.trim(),r[i]||''])));
}
export function toCSV(rows) {if(!rows.length)return '';const keys=[...new Set(rows.flatMap(Object.keys))];const cell=v=>{let s=typeof v==='object'?JSON.stringify(v):String(v??'');if(/^[=+@\-\t\r]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return [keys.map(cell).join(','),...rows.map(r=>keys.map(k=>cell(r[k])).join(','))].join('\r\n');}
export function safeURL(value) {try{const u=new URL(value);return ['http:','https:'].includes(u.protocol)?u.href:null;}catch{return null;}}
