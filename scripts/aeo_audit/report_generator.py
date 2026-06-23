"""
Report generator: Produces markdown audit reports and CSV data exports.
"""

import csv
import json
import os
from datetime import datetime
from analyzer import AuditAnalysis, format_visibility_grade


def generate_markdown_report(analysis: AuditAnalysis, output_dir: str = ".") -> str:
    """Generate a full markdown audit report."""
    
    grade = format_visibility_grade(analysis.client_visibility_rate)
    timestamp = datetime.now().strftime("%B %d, %Y")
    
    lines = []
    lines.append(f"# AI Retrieval Visibility Audit: {analysis.company}")
    lines.append(f"")
    prepared_by = os.environ.get("VISIBILITY_OPS_BRAND", "{brand}")
    prepared_domain = os.environ.get("VISIBILITY_OPS_DOMAIN", "{domain}")
    lines.append(f"**Prepared by:** {prepared_by} | {prepared_domain}")
    lines.append(f"**Date:** {timestamp}")
    lines.append(f"**Queries analyzed:** {analysis.successful_queries}")
    lines.append(f"**Data source:** Perplexity Search API (200B+ indexed URLs)")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # ── EXECUTIVE SUMMARY ──
    lines.append(f"## Executive Summary")
    lines.append(f"")
    lines.append(f"**Visibility Grade: {grade}**")
    lines.append(f"")
    lines.append(
        f"{analysis.company} appears in **{analysis.client_visibility_rate:.0%}** of "
        f"AI search retrieval results across {analysis.successful_queries} queries "
        f"that their target buyers are asking."
    )
    if analysis.client_avg_position > 0:
        lines.append(
            f"When present, the average retrieval position is **#{analysis.client_avg_position:.1f}** "
            f"out of 10."
        )
    lines.append(f"")
    
    # Competitor comparison summary
    if analysis.competitor_stats:
        lines.append(f"### Competitive Comparison")
        lines.append(f"")
        lines.append(f"| Domain | Visibility Rate | Avg Position | Score |")
        lines.append(f"|--------|----------------|-------------|-------|")
        
        # Client row
        lines.append(
            f"| **{analysis.client_domain}** | "
            f"**{analysis.client_visibility_rate:.0%}** | "
            f"**#{analysis.client_avg_position:.1f}** | "
            f"**{analysis.client_visibility_score:.1f}** |"
        )
        
        # Competitor rows
        for domain, stats in sorted(
            analysis.competitor_stats.items(),
            key=lambda x: x[1].visibility_rate,
            reverse=True,
        ):
            lines.append(
                f"| {domain} | "
                f"{stats.visibility_rate:.0%} | "
                f"#{stats.avg_position:.1f} | "
                f"{stats.visibility_score:.1f} |"
            )
        lines.append(f"")
    
    # ── VISIBILITY GAPS ──
    if analysis.gaps:
        lines.append(f"## Visibility Gaps (Competitors Present, You're Not)")
        lines.append(f"")
        lines.append(
            f"These are the {len(analysis.gaps)} queries where at least one competitor "
            f"appears in retrieval results but {analysis.company} does not. "
            f"These represent the highest-priority content opportunities."
        )
        lines.append(f"")
        
        for gap in analysis.gaps:
            comp_list = ", ".join(gap.competitor_domains_present)
            lines.append(f"- **\"{gap.query}\"** ({gap.intent})")
            lines.append(f"  - Competitors present: {comp_list}")
            lines.append(f"  - Top sources: {', '.join(gap.top_domains[:3])}")
        lines.append(f"")
    
    # ── INTENT COVERAGE ──
    if analysis.intent_coverage:
        lines.append(f"## Visibility by Buyer Intent Stage")
        lines.append(f"")
        lines.append(f"| Intent Stage | Present | Absent | Coverage |")
        lines.append(f"|-------------|---------|--------|----------|")
        
        for intent, data in sorted(analysis.intent_coverage.items()):
            total = data["total"]
            present = data["present"]
            rate = present / total if total > 0 else 0
            lines.append(
                f"| {intent.title()} | {present} | {data['absent']} | {rate:.0%} |"
            )
        lines.append(f"")
        lines.append(
            f"*Intent mapping: awareness = educational queries, "
            f"consideration = \"best tool\" listicles, "
            f"comparison = vs/alternative queries, "
            f"brand = direct company name queries*"
        )
        lines.append(f"")
    
    # ── TOP DOMAINS IN RETRIEVAL ──
    lines.append(f"## Top 20 Domains in AI Retrieval Results")
    lines.append(f"")
    lines.append(
        f"These are the domains most frequently surfaced by Perplexity's retrieval "
        f"index for your target query set. These are the sources AI search engines "
        f"are pulling from to answer questions about your category."
    )
    lines.append(f"")
    lines.append(f"| Rank | Domain | Appearances | Visibility Rate | Avg Position |")
    lines.append(f"|------|--------|-------------|----------------|-------------|")
    
    for i, ds in enumerate(analysis.domain_rankings[:20], 1):
        marker = ""
        if ds.domain == analysis.client_domain:
            marker = " ⭐"
        elif ds.domain in [d for d in analysis.competitor_stats]:
            marker = " 🔴"
        lines.append(
            f"| {i} | {ds.domain}{marker} | "
            f"{ds.appearances}/{ds.total_queries} | "
            f"{ds.visibility_rate:.0%} | "
            f"#{ds.avg_position:.1f} |"
        )
    lines.append(f"")
    lines.append(f"*⭐ = client, 🔴 = competitor*")
    lines.append(f"")
    
    # ── TOP CITED URLs ──
    if analysis.top_urls:
        lines.append(f"## Top Cited URLs")
        lines.append(f"")
        lines.append(
            f"These specific pages are getting retrieved most frequently. "
            f"Study their structure — this is what gets cited by AI."
        )
        lines.append(f"")
        for url, count in analysis.top_urls[:15]:
            lines.append(f"- ({count}x) {url}")
        lines.append(f"")
    
    # ── QUERIES WHERE CLIENT APPEARS ──
    if analysis.client_queries_present:
        lines.append(f"## Queries Where {analysis.company} Appears")
        lines.append(f"")
        for q in analysis.client_queries_present:
            lines.append(f"- ✅ \"{q}\"")
        lines.append(f"")
    
    # ── QUERIES WHERE CLIENT IS ABSENT ──
    if analysis.client_queries_absent:
        lines.append(f"## Queries Where {analysis.company} Is Absent")
        lines.append(f"")
        for q in analysis.client_queries_absent:
            lines.append(f"- ❌ \"{q}\"")
        lines.append(f"")
    
    # ── RECOMMENDATIONS ──
    lines.append(f"## Recommended Actions")
    lines.append(f"")
    
    if analysis.client_visibility_rate < 0.2:
        lines.append(
            f"**Priority: Foundation building.** {analysis.company} has minimal AI search "
            f"visibility. Focus on creating definitive, well-structured content for the "
            f"top 5 gap queries identified above. Structure content with clear definitions, "
            f"step-by-step frameworks, and FAQ sections that LLMs can easily extract and cite."
        )
    elif analysis.client_visibility_rate < 0.5:
        lines.append(
            f"**Priority: Gap closing.** {analysis.company} has partial visibility but "
            f"significant gaps, especially in comparison and consideration queries. "
            f"Create comparison pages, \"alternatives\" content, and category listicle-style "
            f"content optimized for AI retrieval."
        )
    else:
        lines.append(
            f"**Priority: Position improvement.** {analysis.company} has solid retrieval "
            f"presence. Focus on improving ranking position within results — restructure "
            f"existing content for AI citability and build additional authority content "
            f"around gap queries."
        )
    lines.append(f"")
    
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Report generated using Perplexity Search API retrieval data.*")
    lines.append(f"*This shows which sources Perplexity's index retrieves and ranks — ")
    lines.append(f"the same retrieval layer powering 200M+ daily AI search queries.*")
    
    report = "\n".join(lines)
    
    # Write file
    slug = analysis.company.lower().replace(" ", "-")
    filepath = os.path.join(output_dir, f"audit-report-{slug}.md")
    with open(filepath, "w") as f:
        f.write(report)
    
    return filepath


def generate_domain_csv(analysis: AuditAnalysis, output_dir: str = ".") -> str:
    """Export domain visibility data as CSV."""
    slug = analysis.company.lower().replace(" ", "-")
    filepath = os.path.join(output_dir, f"domain-visibility-{slug}.csv")
    
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "domain", "appearances", "total_queries",
            "visibility_rate", "avg_position", "visibility_score",
            "is_client", "is_competitor", "queries_appeared_in",
        ])
        
        for i, ds in enumerate(analysis.domain_rankings, 1):
            writer.writerow([
                i,
                ds.domain,
                ds.appearances,
                ds.total_queries,
                f"{ds.visibility_rate:.3f}",
                f"{ds.avg_position:.1f}",
                f"{ds.visibility_score:.1f}",
                ds.domain == analysis.client_domain,
                ds.domain in analysis.competitor_stats,
                "; ".join(ds.queries_appeared_in[:10]),
            ])
    
    return filepath


def generate_raw_json(
    results: list, analysis: AuditAnalysis, output_dir: str = "."
) -> str:
    """Export complete raw results as JSON for further analysis."""
    slug = analysis.company.lower().replace(" ", "-")
    filepath = os.path.join(output_dir, f"raw-results-{slug}.json")
    
    data = {
        "company": analysis.company,
        "client_domain": analysis.client_domain,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_queries": analysis.total_queries,
            "successful": analysis.successful_queries,
            "visibility_rate": analysis.client_visibility_rate,
            "avg_position": analysis.client_avg_position,
            "visibility_score": analysis.client_visibility_score,
        },
        "results": [],
    }
    
    for qr in results:
        entry = {
            "query": qr.query,
            "error": qr.error,
            "answer_text": qr.answer_text[:2000] if qr.answer_text else "",
            "citations": qr.citations,
            "results": [],
        }
        for sr in qr.results:
            entry["results"].append({
                "title": sr.title,
                "url": sr.url,
                "domain": sr.domain,
                "position": sr.position,
                "snippet": sr.snippet[:300],
                "date": sr.date,
            })
        data["results"].append(entry)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    return filepath
