#!/usr/bin/env python3
from __future__ import annotations

"""
AEO Retrieval Audit Tool
========================

Uses Perplexity's Search API to run programmatic AI visibility audits.
See CLAUDE.md for full documentation.

Usage:
    python aeo_audit.py audit --company "Avoma" --domain "avoma.com" \
        --category "conversation intelligence" --competitors "gong.io,chorus.ai"
    
    python aeo_audit.py cluster --queries "best AEO tools,AI search optimization" \
        --track-domain "acme.com"
    
    python aeo_audit.py batch --input queries.csv --output results/
"""

import argparse
import asyncio
import csv
import json as json_mod
import logging
import os
import sys

# Resolve paths relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, SCRIPT_DIR)

# Load .env from repo root
from dotenv import load_dotenv
load_dotenv(os.path.join(REPO_ROOT, ".env"))

from perplexity_client import PerplexityClient
from query_templates import generate_audit_queries, generate_cluster_queries
from analyzer import AuditAnalyzer
from report_generator import (
    generate_markdown_report,
    generate_domain_csv,
    generate_raw_json,
)
from metrics_calculator import (
    calculate_query_metrics,
    aggregate_batch_metrics,
    analyze_sentiment,
)

# Client workspace registry for output routing
CLIENTS_REGISTRY = os.path.join(REPO_ROOT, "clients_registry.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def resolve_output_dir(client_slug: str | None, fallback: str = "./results") -> str:
    """Resolve output directory. Routes to client workspace if --client is provided."""
    if not client_slug:
        return fallback

    # Check clients_registry.json for path
    if os.path.exists(CLIENTS_REGISTRY):
        with open(CLIENTS_REGISTRY) as f:
            registry = json_mod.load(f)
        if client_slug in registry:
            client_root = registry[client_slug]
            if not os.path.isabs(client_root):
                client_root = os.path.join(REPO_ROOT, client_root)
            audit_dir = os.path.join(client_root, "04_content_engine", "audits")
            os.makedirs(audit_dir, exist_ok=True)
            return audit_dir

    # Fallback: ../clients/{slug}/04_content_engine/audits/
    client_root = os.path.join(REPO_ROOT, "..", "clients", client_slug)
    if os.path.isdir(client_root):
        audit_dir = os.path.join(client_root, "04_content_engine", "audits")
        os.makedirs(audit_dir, exist_ok=True)
        return audit_dir

    return fallback


async def run_audit(args):
    """Full company audit: generate queries, search, analyze, report."""
    competitors = []
    if args.competitors:
        competitors = [c.strip() for c in args.competitors.split(",")]
    
    extra_queries = []
    if args.extra_queries:
        extra_queries = [q.strip() for q in args.extra_queries.split(",")]
    
    # Generate queries
    query_metadata = generate_audit_queries(
        company=args.company,
        domain=args.domain,
        category=args.category,
        competitors=competitors,
        icp=args.icp or "B2B SaaS",
        extra_queries=extra_queries,
    )
    
    queries = [qm["query"] for qm in query_metadata]
    
    logger.info(f"Generated {len(queries)} audit queries for {args.company}")
    logger.info(f"Estimated cost: ${len(queries) * 0.005:.3f}")
    
    # Run searches
    client = PerplexityClient(
        max_concurrent=args.concurrency or 3,
        max_results_per_query=args.max_results or 10,
    )
    
    try:
        logger.info("Running queries against Perplexity Search API...")
        results = await client.search_batch(queries)
        
        successful = sum(1 for r in results if r.error is None)
        logger.info(f"Completed: {successful}/{len(results)} queries successful")
        
        # Analyze (legacy domain-based analysis)
        analyzer = AuditAnalyzer(
            company=args.company,
            client_domain=args.domain,
            competitor_domains=competitors,
        )
        analysis = analyzer.analyze(results, query_metadata)

        # ── New metrics: answer-text + citation based ──
        comp_list = [
            {"name": c.replace(".com", "").replace(".io", "").replace(".ai", "").title(),
             "domain": c}
            for c in competitors
        ]

        per_query_metrics = []
        for qr in results:
            if qr.error:
                continue
            pqm = calculate_query_metrics(
                answer_text=qr.answer_text,
                citations=qr.citations,
                query=qr.query,
                client_domain=args.domain,
                client_brand_name=args.company,
                competitor_list=comp_list,
            )

            # Sentiment analysis (optional, per-query)
            if getattr(args, "sentiment", False):
                pqm.sentiment = await analyze_sentiment(
                    qr.answer_text, args.company,
                )

            per_query_metrics.append(pqm)

        batch_metrics = aggregate_batch_metrics(
            per_query_metrics,
            company=args.company,
            client_domain=args.domain,
            competitor_list=comp_list,
        )

        # Generate reports - route to client workspace if --client provided
        output_dir = resolve_output_dir(
            getattr(args, "client", None), args.output or "./results"
        )
        os.makedirs(output_dir, exist_ok=True)

        md_path = generate_markdown_report(analysis, output_dir)
        csv_path = generate_domain_csv(analysis, output_dir)
        json_path = generate_raw_json(results, analysis, output_dir)
        metrics_path = _write_metrics_json(batch_metrics, output_dir)

        logger.info(f"")
        logger.info(f"{'='*60}")
        logger.info(f"AUDIT COMPLETE: {args.company}")
        logger.info(f"{'='*60}")
        logger.info(f"Visibility Grade: {_grade(analysis.client_visibility_rate)}")
        logger.info(f"Answer Rate: {batch_metrics.answer_rate:.1f}%")
        logger.info(f"Avg Citation Score: {batch_metrics.avg_citation_score:.2f}/3")
        logger.info(f"Share of Voice: {batch_metrics.share_of_voice.get(args.company, 0):.1f}%")
        logger.info(f"Avg Prominence: {batch_metrics.avg_prominence:.1f}%")
        logger.info(f"Source Control: {batch_metrics.source_control_rate:.1f}%")
        logger.info(f"Presence: {batch_metrics.presence_counts}")
        if any(v > 0 for v in batch_metrics.sentiment_distribution.values()):
            logger.info(f"Sentiment: {batch_metrics.sentiment_distribution}")
        logger.info(f"Gaps Found: {len(analysis.gaps)}")
        logger.info(f"")
        logger.info(f"Reports:")
        logger.info(f"  📄 {md_path}")
        logger.info(f"  📊 {csv_path}")
        logger.info(f"  🗂️  {json_path}")
        logger.info(f"  📈 {metrics_path}")
        
    finally:
        await client.close()


async def run_cluster(args):
    """Cluster analysis: run query variations and map domain visibility."""
    if args.queries:
        queries = [q.strip() for q in args.queries.split(",")]
    else:
        queries = generate_cluster_queries(args.topic or "AI marketing tools")
        queries = [q["query"] for q in queries]
    
    logger.info(f"Running cluster analysis: {len(queries)} queries")
    
    client = PerplexityClient(
        max_concurrent=args.concurrency or 3,
        max_results_per_query=args.max_results or 10,
    )
    
    try:
        results = await client.search_batch(queries)
        
        track_domain = (args.track_domain or "").replace("www.", "").lower()
        
        # Quick analysis output
        from collections import Counter, defaultdict
        domain_counter = Counter()
        domain_positions = defaultdict(list)
        
        for qr in results:
            if qr.error:
                continue
            print(f"\n{'─'*60}")
            print(f"Query: \"{qr.query}\"")
            
            tracked_found = False
            for sr in qr.results:
                domain = sr.domain.lower()
                domain_counter[domain] += 1
                domain_positions[domain].append(sr.position + 1)
                
                marker = ""
                if track_domain and track_domain in domain:
                    marker = " ⭐ TRACKED"
                    tracked_found = True
                
                print(f"  #{sr.position + 1}: {sr.domain} — {sr.title[:60]}{marker}")
            
            if track_domain and not tracked_found:
                print(f"  ❌ {track_domain} NOT FOUND in results")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"DOMAIN FREQUENCY (top 15)")
        print(f"{'='*60}")
        for domain, count in domain_counter.most_common(15):
            positions = domain_positions[domain]
            avg_pos = sum(positions) / len(positions)
            marker = " ⭐" if track_domain and track_domain in domain else ""
            print(f"  {domain}: {count} appearances, avg position #{avg_pos:.1f}{marker}")
        
        if track_domain:
            tc = domain_counter.get(track_domain, 0)
            total = sum(1 for r in results if r.error is None)
            print(f"\n📊 {track_domain}: appeared in {tc}/{total} queries ({tc/total:.0%})")
    
    finally:
        await client.close()


async def run_batch(args):
    """Batch mode: read queries from CSV and run."""
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
    
    queries = []
    metadata = []
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            queries.append(row["query"])
            metadata.append({
                "query": row["query"],
                "intent": row.get("category", "custom"),
                "category": row.get("category", "custom"),
            })
    
    logger.info(f"Loaded {len(queries)} queries from {args.input}")
    
    # Determine client domain from CSV or args
    client_domain = args.domain or ""
    if not client_domain and "client_domain" in metadata[0]:
        client_domain = metadata[0].get("client_domain", "")
    
    client = PerplexityClient(
        max_concurrent=args.concurrency or 3,
        max_results_per_query=args.max_results or 10,
    )
    
    try:
        results = await client.search_batch(queries)
        
        if client_domain:
            company_name = args.company or client_domain
            analyzer = AuditAnalyzer(
                company=company_name,
                client_domain=client_domain,
            )
            analysis = analyzer.analyze(results, metadata)

            # New metrics from answer text + citations
            per_query_metrics = []
            for qr in results:
                if qr.error:
                    continue
                pqm = calculate_query_metrics(
                    answer_text=qr.answer_text,
                    citations=qr.citations,
                    query=qr.query,
                    client_domain=client_domain,
                    client_brand_name=company_name,
                )
                per_query_metrics.append(pqm)

            batch_metrics = aggregate_batch_metrics(
                per_query_metrics,
                company=company_name,
                client_domain=client_domain,
            )

            output_dir = resolve_output_dir(
                getattr(args, "client", None), args.output or "./results"
            )
            os.makedirs(output_dir, exist_ok=True)

            md_path = generate_markdown_report(analysis, output_dir)
            csv_path = generate_domain_csv(analysis, output_dir)
            json_path = generate_raw_json(results, analysis, output_dir)
            metrics_path = _write_metrics_json(batch_metrics, output_dir)

            logger.info(f"Reports: {md_path}, {csv_path}, {json_path}, {metrics_path}")
        else:
            # Just dump results
            output_dir = resolve_output_dir(
                getattr(args, "client", None), args.output or "./results"
            )
            os.makedirs(output_dir, exist_ok=True)
            outpath = os.path.join(output_dir, "batch-results.json")
            data = []
            for qr in results:
                entry = {"query": qr.query, "error": qr.error, "results": []}
                for sr in qr.results:
                    entry["results"].append({
                        "title": sr.title, "url": sr.url,
                        "domain": sr.domain, "position": sr.position,
                    })
                data.append(entry)
            with open(outpath, "w") as f:
                json_mod.dump(data, f, indent=2)
            logger.info(f"Results written to {outpath}")
    
    finally:
        await client.close()


def _write_metrics_json(batch_metrics, output_dir: str) -> str:
    """Write batch metrics to JSON."""
    from dataclasses import asdict
    slug = batch_metrics.company.lower().replace(" ", "-")
    filepath = os.path.join(output_dir, f"metrics-{slug}.json")

    # Build serializable dict (avoid nested dataclass issues)
    data = {
        "company": batch_metrics.company,
        "client_domain": batch_metrics.client_domain,
        "total_queries": batch_metrics.total_queries,
        "successful_queries": batch_metrics.successful_queries,
        "answer_rate": batch_metrics.answer_rate,
        "share_of_voice": batch_metrics.share_of_voice,
        "avg_prominence": batch_metrics.avg_prominence,
        "source_control_rate": batch_metrics.source_control_rate,
        "sentiment_distribution": batch_metrics.sentiment_distribution,
        "presence_counts": batch_metrics.presence_counts,
        "avg_citation_score": batch_metrics.avg_citation_score,
        "per_query": [],
    }

    for pqm in batch_metrics.query_metrics:
        entry = {
            "query": pqm.query,
            "presence_type": pqm.brand_presence.presence_type,
            "citation_score": pqm.brand_presence.citation_score,
            "brand_mentioned": pqm.brand_presence.brand_mentioned,
            "source_cited": pqm.brand_presence.source_cited,
            "client_citation_count": pqm.citation_analysis.client_citation_count,
            "client_citation_positions": pqm.citation_analysis.client_citation_positions,
            "competitor_citations": {
                k: len(v) for k, v in pqm.citation_analysis.competitor_citations.items()
            },
            "brand_position_pct": pqm.prominence.brand_position_pct,
            "is_first_cited": pqm.prominence.is_first_cited,
            "is_first_mentioned": pqm.prominence.is_first_mentioned,
            "source_control_rate": pqm.source_control.source_control_rate,
        }
        if pqm.sentiment:
            entry["sentiment"] = {
                "label": pqm.sentiment.sentiment_label,
                "characterization": pqm.sentiment.characterization_text,
            }
        data["per_query"].append(entry)

    with open(filepath, "w") as f:
        json_mod.dump(data, f, indent=2)

    return filepath


def _grade(rate: float) -> str:
    if rate >= 0.8: return "A"
    elif rate >= 0.6: return "B"
    elif rate >= 0.4: return "C"
    elif rate >= 0.2: return "D"
    else: return "F"


def main():
    parser = argparse.ArgumentParser(
        description="AEO Retrieval Audit Tool — Perplexity Search API"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # ── AUDIT command ──
    audit_p = subparsers.add_parser("audit", help="Full company visibility audit")
    audit_p.add_argument("--company", required=True, help="Company name")
    audit_p.add_argument("--domain", required=True, help="Company domain (e.g. avoma.com)")
    audit_p.add_argument("--category", required=True, help="Product category (e.g. conversation intelligence)")
    audit_p.add_argument("--competitors", help="Comma-separated competitor domains")
    audit_p.add_argument("--icp", default="B2B SaaS", help="Ideal customer profile descriptor")
    audit_p.add_argument("--extra-queries", help="Comma-separated additional queries")
    audit_p.add_argument("--client", help="Client slug - routes output to client workspace audits folder")
    audit_p.add_argument("--output", default="./results", help="Output directory (ignored if --client set)")
    audit_p.add_argument("--concurrency", type=int, default=3, help="Max concurrent requests")
    audit_p.add_argument("--max-results", type=int, default=10, help="Results per query (1-20)")
    audit_p.add_argument("--sentiment", action="store_true", help="Run sentiment analysis via Claude API (adds ~$0.01/query)")
    
    # ── CLUSTER command ──
    cluster_p = subparsers.add_parser("cluster", help="Query cluster domain analysis")
    cluster_p.add_argument("--queries", help="Comma-separated queries")
    cluster_p.add_argument("--topic", help="Topic to auto-generate query variations for")
    cluster_p.add_argument("--track-domain", help="Domain to track across all queries")
    cluster_p.add_argument("--concurrency", type=int, default=3)
    cluster_p.add_argument("--max-results", type=int, default=10)
    
    # ── BATCH command ──
    batch_p = subparsers.add_parser("batch", help="Batch queries from CSV")
    batch_p.add_argument("--input", required=True, help="CSV file with queries")
    batch_p.add_argument("--domain", help="Client domain to track")
    batch_p.add_argument("--company", help="Company name for reports")
    batch_p.add_argument("--client", help="Client slug - routes output to client workspace audits folder")
    batch_p.add_argument("--output", default="./results", help="Output directory (ignored if --client set)")
    batch_p.add_argument("--concurrency", type=int, default=3)
    batch_p.add_argument("--max-results", type=int, default=10)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "audit":
        asyncio.run(run_audit(args))
    elif args.command == "cluster":
        asyncio.run(run_cluster(args))
    elif args.command == "batch":
        asyncio.run(run_batch(args))


if __name__ == "__main__":
    main()
