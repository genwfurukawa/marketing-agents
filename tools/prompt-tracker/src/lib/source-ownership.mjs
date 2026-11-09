// Explicit ownership only. Inventory is crawled; competitor rules classify citations only.
export function domainHost(value) {
  const url = new URL(value.includes('://') ? value : 'https://' + value.trim());
  if (url.protocol !== 'https:' || url.username || url.password || url.port ||
      url.pathname !== '/' || url.search || url.hash || !url.hostname.includes('.') ||
      !/^[a-z0-9.-]+$/i.test(url.hostname) || /^\d[\d.]+$/.test(url.hostname)) {
    throw Error('Enter a public domain or subdomain, without a path or port.');
  }
  return url.hostname.toLowerCase().replace(/^www\./, '').replace(/\.$/, '');
}

export function registeredDomain(project,host) {
  return [project.domain,...(project.ownedDomains||[])].filter(Boolean).some(value=>{try{return domainHost(value)===host;}catch{return false;}});
}

export function sourceOwner(url,project) {
  let host;try{host=new URL(url).hostname.toLowerCase().replace(/^www\./,'');}catch{return {kind:'Third-party',name:''};}
  const matches=domain=>{try{const d=new URL(domain.includes('://')?domain:'https://'+domain).hostname.toLowerCase().replace(/^www\./,'');return host===d||host.endsWith('.'+d);}catch{return false;}};
  if([project.domain,...(project.ownedDomains||[])].filter(Boolean).some(matches))return {kind:'First-party',name:project.name};
  const competitor=(project.competitorDomains||[]).filter(rule=>(project.competitors||[]).includes(rule.name)&&matches(rule.domain)).sort((a,b)=>b.domain.length-a.domain.length)[0];
  return competitor?{kind:'Competitor',name:competitor.name}:{kind:'Third-party',name:''};
}
