#!/usr/bin/env python3
"""
aeo_audit.py: the reference implementation.

Runs a bank of buyer questions against one AI answer engine and records who got
cited. Emits the same files, and the same JSON shape, that the skills in this repo
expect, so `build-audit-report`, `build-query-bank`, `aeo-engine-scan` and
`competitive-monitor` all work against it.

This is deliberately the simple version: one engine, one pass, no concurrency, no
sentiment, no cross-engine merge. It is enough to get a real baseline and to re-run
that baseline on a schedule, which is the part that matters.

    export PERPLEXITY_API_KEY=...
    python3 scripts/aeo_audit/aeo_audit.py batch \
        --input queries.csv --domain acme.com --company "Acme" --output ./results

Input CSV needs a `query` column. `category` and `client_domain` are optional.

Outputs, written to --output:
    metrics-{slug}.json        the scores, per query and aggregate
    raw-results-{slug}.json    the full answer text and citations for every query
    audit-report-{slug}.md     a readable summary

Scoring, 0 to 3 per query:
    0 absent     you are not in the answer
    1 mentioned  your brand name appears, but nothing of yours is cited
    2 cited      your domain is among the sources
    3 featured   your domain is cited in the first third of the sources

Aggregates: answer rate (how often you appear at all), share of voice (your
mentions against named rivals), and source control rate (citations you own against
citations you do not).
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone

SCORE = {"absent": 0, "mentioned": 1, "cited": 2, "featured": 3}
SUPPORTED_ENGINES = ("perplexity",)
API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = os.environ.get("AEO_MODEL", "sonar")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "brand").lower()).strip("-") or "brand"


def domain_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).lower().replace("www.", "") if m else ""


def ask(query, api_key, timeout=60):
    """One query against the engine. Returns (answer_text, [citation urls])."""
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": query}],
    }).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.load(resp)
    text = data["choices"][0]["message"]["content"]
    # Perplexity returns citations at the top level; newer payloads use search_results.
    cites = data.get("citations") or [
        r.get("url", "") for r in data.get("search_results", [])
    ]
    return text, [c for c in cites if c]


def score_one(query, answer, citations, brand, domain, competitors):
    """Score a single answer. Mirrors the presence taxonomy in the docstring."""
    cite_domains = [domain_of(u) for u in citations]
    brand_in_text = bool(brand) and brand.lower() in (answer or "").lower()
    own = [i for i, d in enumerate(cite_domains) if d and d.endswith(domain)]

    if own:
        # Featured if the first owned citation lands in the first third of sources.
        first_third = max(1, len(cite_domains) // 3)
        presence = "featured" if own[0] < first_third else "cited"
    elif brand_in_text:
        presence = "mentioned"
    else:
        presence = "absent"

    rivals = {}
    for c in competitors:
        c = c.strip()
        if not c:
            continue
        name = c.split(".")[0]
        hits = sum(1 for d in cite_domains if d and d.endswith(c))
        in_text = name.lower() in (answer or "").lower()
        if hits or in_text:
            rivals[c] = {"cited": hits, "mentioned": in_text}

    third_party = sum(1 for d in cite_domains if d and not d.endswith(domain))
    return {
        "query": query,
        "presence_type": presence,
        "citation_score": SCORE[presence],
        "brand_mentioned": brand_in_text,
        "source_cited": bool(own),
        "brand_position": own[0] + 1 if own else None,
        "total_citations": len(cite_domains),
        "own_citations": len(own),
        "third_party_citations": third_party,
        "competitors_present": rivals,
        "citation_domains": cite_domains,
    }


def aggregate(rows, brand, competitors):
    total = len(rows) or 1
    present = [r for r in rows if r["presence_type"] != "absent"]
    positions = [r["brand_position"] for r in rows if r["brand_position"]]

    mentions = Counter()
    mentions[brand] = sum(1 for r in rows if r["brand_mentioned"] or r["source_cited"])
    for c in competitors:
        c = c.strip()
        if c:
            mentions[c] = sum(1 for r in rows if c in r["competitors_present"])
    total_mentions = sum(mentions.values()) or 1

    own = sum(r["own_citations"] for r in rows)
    third = sum(r["third_party_citations"] for r in rows)

    return {
        "total_queries": len(rows),
        "answer_rate": round(len(present) / total * 100, 1),
        "avg_citation_score": round(sum(r["citation_score"] for r in rows) / total, 2),
        "share_of_voice": {k: round(v / total_mentions * 100, 1)
                           for k, v in mentions.items() if v},
        "avg_prominence": round(sum(positions) / len(positions), 1) if positions else None,
        "source_control_rate": round(own / (own + third) * 100, 1) if (own + third) else 0.0,
        "presence_breakdown": dict(Counter(r["presence_type"] for r in rows)),
    }


def write_report(path, company, domain, agg, rows):
    def bar(n, total, width=24):
        filled = int(round(width * n / total)) if total else 0
        return "#" * filled + "." * (width - filled)

    total = agg["total_queries"]
    lines = [
        f"# AI visibility baseline: {company}",
        "",
        f"`{domain}` across {total} buyer questions, "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.",
        "",
        "## Where you stand",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Answer rate | {agg['answer_rate']}% of questions mention or cite you |",
        f"| Average citation score | {agg['avg_citation_score']} out of 3 |",
        f"| Source control rate | {agg['source_control_rate']}% of citations are yours |",
        f"| Average position when cited | "
        f"{agg['avg_prominence'] if agg['avg_prominence'] else 'not cited'} |",
        "",
        "## Presence breakdown",
        "",
        "```",
    ]
    for k in ("featured", "cited", "mentioned", "absent"):
        n = agg["presence_breakdown"].get(k, 0)
        lines.append(f"{k:<10} {bar(n, total)} {n:>3}  ({round(100*n/total) if total else 0}%)")
    lines += ["```", "", "## Share of voice", "", "| Brand | Share |", "|---|---|"]
    for b, pct in sorted(agg["share_of_voice"].items(), key=lambda x: -x[1]):
        lines.append(f"| {'**' + b + '**' if b.lower().startswith(company.lower()[:6]) else b} | {pct}% |")

    absent = [r for r in rows if r["presence_type"] == "absent"]
    if absent:
        noun = "question" if len(absent) == 1 else "questions"
        lines += ["", f"## The {len(absent)} {noun} you are absent from", ""]
        lines += [f"- {r['query']}" for r in absent[:25]]
        if len(absent) > 25:
            lines.append(f"- ...and {len(absent) - 25} more, see the metrics JSON")

    lines += [
        "",
        "## Reading this",
        "",
        "One run is a screenshot. Re-run the same bank on a schedule and report the",
        "delta against this baseline. An absolute score is not meaningful on its own,",
        "and no one can promise you a ranking.",
        "",
        "Raw answer text and every citation are in the `raw-results-*.json` alongside.",
        "",
    ]
    with open(path, "w") as f:
        f.write("\n".join(lines))


# Enough coverage to get a real baseline. Widen it with `build-query-bank`, which
# mines actual buyer questions rather than permuting a category name.
TEMPLATES = [
    ("consideration", "best {category} tools"),
    ("consideration", "top {category} software"),
    ("consideration", "{category} for {icp}"),
    ("definition",    "what is {category}"),
    ("problem",       "how to choose {category} software"),
    ("comparison",    "{company} vs {rival}"),
    ("comparison",    "alternatives to {rival}"),
    ("comparison",    "best {rival} alternatives"),
]


def build_queries(company, category, icp, competitors):
    """Generate a starter bank. Deterministic, so re-runs compare cleanly."""
    rivals = [c.strip().split(".")[0] for c in competitors if c.strip()] or [""]
    seen, rows = set(), []
    for cat, tpl in TEMPLATES:
        targets = rivals if "{rival}" in tpl else [""]
        for rival in targets:
            q = tpl.format(category=category, icp=icp, company=company, rival=rival)
            q = re.sub(r"\s+", " ", q).strip()
            if q.lower() not in seen:
                seen.add(q.lower())
                rows.append({"query": q, "category": cat})
    return rows


def resolve_engines(requested):
    """Return (to_run, skipped). This build ships one engine on purpose."""
    if not requested:
        return list(SUPPORTED_ENGINES), []
    asked = [e.strip().lower() for e in requested.split(",") if e.strip()]
    run = [e for e in asked if e in SUPPORTED_ENGINES]
    skipped = [e for e in asked if e not in SUPPORTED_ENGINES]
    return (run or list(SUPPORTED_ENGINES)), skipped


def announce_engines(requested):
    run, skipped = resolve_engines(requested)
    if skipped:
        print(f"  engines: running {', '.join(run)}; "
              f"skipping {', '.join(skipped)} (not in the reference build)")
    return run, skipped


def cmd_audit(args):
    """Generate a starter query bank, then score it."""
    company = args.company
    rows = build_queries(company, args.category, args.icp,
                         (args.competitors or "").split(","))
    os.makedirs(args.output, exist_ok=True)
    bank = os.path.join(args.output, f"query-bank-{slugify(company)}.csv")
    with open(bank, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["query", "category", "client_domain"])
        w.writeheader()
        for r in rows:
            w.writerow({**r, "client_domain": args.domain})
    print(f"  wrote {bank} ({len(rows)} queries)")
    args.input = bank
    return cmd_batch(args)


def cmd_batch(args):
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        sys.exit("PERPLEXITY_API_KEY is not set. Export it and re-run.")

    if not os.path.exists(args.input):
        sys.exit(f"No such input file: {args.input}")

    with open(args.input, newline="") as f:
        queries = [r for r in csv.DictReader(f) if (r.get("query") or "").strip()]
    if not queries:
        sys.exit(f"No rows with a 'query' column in {args.input}")

    _run, skipped = announce_engines(getattr(args, "engines", None))
    domain = (args.domain or "").lower().replace("www.", "")
    company = args.company or domain.split(".")[0].title()
    competitors = (args.competitors or "").split(",") if args.competitors else []
    os.makedirs(args.output, exist_ok=True)
    slug = slugify(company)

    rows, raw = [], []
    for i, row in enumerate(queries, 1):
        q = row["query"].strip()
        print(f"  [{i}/{len(queries)}] {q[:68]}", flush=True)
        try:
            answer, citations = ask(q, api_key)
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            print(f"      failed: {e}. Recorded as absent.", file=sys.stderr)
            answer, citations = "", []
        scored = score_one(q, answer, citations, company, domain, competitors)
        scored["category"] = (row.get("category") or "").strip()
        rows.append(scored)
        raw.append({"query": q, "answer": answer, "citations": citations})
        time.sleep(args.delay)

    agg = aggregate(rows, company, competitors)
    out = {
        "company": company,
        "client_domain": domain,
        "engine": MODEL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reference_implementation": True,
        "engines_run": list(SUPPORTED_ENGINES),
        "engines_skipped": [{"engine": e, "reason": "not in the reference build"}
                            for e in skipped],
        "aggregate": agg,
        "queries": rows,
    }

    mpath = os.path.join(args.output, f"metrics-{slug}.json")
    rpath = os.path.join(args.output, f"raw-results-{slug}.json")
    dpath = os.path.join(args.output, f"audit-report-{slug}.md")
    with open(mpath, "w") as f:
        json.dump(out, f, indent=2)
    with open(rpath, "w") as f:
        json.dump(raw, f, indent=2)
    write_report(dpath, company, domain, agg, rows)

    print(f"\n  answer rate        {agg['answer_rate']}%")
    print(f"  avg citation score {agg['avg_citation_score']} / 3")
    print(f"  source control     {agg['source_control_rate']}%")
    print(f"\n  wrote {mpath}\n        {rpath}\n        {dpath}")


def main():
    p = argparse.ArgumentParser(
        description="Reference AI visibility audit. One engine, one pass.")
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("batch", help="Run a CSV query bank")
    b.add_argument("--input", required=True, help="CSV with a 'query' column")
    b.add_argument("--domain", required=True, help="Your domain, e.g. acme.com")
    b.add_argument("--company", help="Brand name as it appears in prose")
    b.add_argument("--competitors", help="Comma-separated rival domains")
    b.add_argument("--output", default="./results", help="Output directory")
    b.add_argument("--delay", type=float, default=1.0,
                   help="Seconds between calls. Raise it if you get rate limited.")
    b.add_argument("--engines", help="Comma-separated engines. This build runs "
                                     "perplexity; others are reported as skipped.")
    b.set_defaults(func=cmd_batch)

    a = sub.add_parser("audit", help="Generate a starter query bank, then score it")
    a.add_argument("--company", required=True)
    a.add_argument("--domain", required=True)
    a.add_argument("--category", required=True,
                   help="Product category, e.g. 'conversation intelligence'")
    a.add_argument("--icp", default="B2B SaaS", help="Who it is for")
    a.add_argument("--competitors", help="Comma-separated rival domains")
    a.add_argument("--output", default="./results")
    a.add_argument("--delay", type=float, default=1.0)
    a.add_argument("--engines", help="Comma-separated engines")
    a.set_defaults(func=cmd_audit)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
