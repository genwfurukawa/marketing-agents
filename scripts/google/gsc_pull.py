#!/usr/bin/env python3
"""Pull Search Console queries + pages. CSVs + a markdown summary into research/gsc/."""
import os
import csv
import argparse
from datetime import date, timedelta
from pathlib import Path
from googleapiclient.discovery import build
from auth import get_credentials


def fetch(service, site, start, end, dimensions, row_limit=1000):
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    return service.searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])


def write_csv(path: Path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=28)
    parser.add_argument("--out", default="research/gsc")
    args = parser.parse_args()

    site = os.environ["GSC_SITE_URL"]
    end = date.today() - timedelta(days=2)  # GSC has ~2 day lag
    start = end - timedelta(days=args.days)
    out_dir = Path(args.out)
    today = date.today().isoformat()

    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    queries = fetch(service, site, start.isoformat(), end.isoformat(), ["query"])
    write_csv(
        out_dir / f"{today}_queries.csv",
        ["query", "clicks", "impressions", "ctr", "position"],
        [[r["keys"][0], r["clicks"], r["impressions"], r["ctr"], r["position"]] for r in queries],
    )

    pages = fetch(service, site, start.isoformat(), end.isoformat(), ["page"])
    write_csv(
        out_dir / f"{today}_pages.csv",
        ["page", "clicks", "impressions", "ctr", "position"],
        [[r["keys"][0], r["clicks"], r["impressions"], r["ctr"], r["position"]] for r in pages],
    )

    total_clicks = sum(r["clicks"] for r in queries)
    total_impr = sum(r["impressions"] for r in queries)
    avg_ctr = (total_clicks / total_impr) if total_impr else 0

    top_q = sorted(queries, key=lambda r: r["clicks"], reverse=True)[:20]
    fix_candidates = sorted(
        [r for r in queries if r["impressions"] >= 100 and r["ctr"] < 0.02],
        key=lambda r: r["impressions"], reverse=True,
    )[:20]
    top_pages = sorted(pages, key=lambda r: r["clicks"], reverse=True)[:20]

    summary = out_dir / f"{today}_summary.md"
    with open(summary, "w") as f:
        f.write(f"# GSC Summary — {today}\n\n")
        f.write(f"- Site: `{site}`\n")
        f.write(f"- Window: {start} → {end} ({args.days} days)\n")
        f.write(f"- Total clicks: **{total_clicks}**\n")
        f.write(f"- Total impressions: **{total_impr}**\n")
        f.write(f"- Avg CTR: **{avg_ctr*100:.2f}%**\n\n")

        f.write("## Top 20 queries by clicks\n\n")
        f.write("| Query | Clicks | Impressions | CTR | Position |\n|---|---|---|---|---|\n")
        for r in top_q:
            f.write(f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.2f}% | {r['position']:.1f} |\n")

        f.write("\n## High impressions, low CTR — snippet/title fix candidates (≥100 impr, <2% CTR)\n\n")
        f.write("| Query | Impressions | CTR | Position |\n|---|---|---|---|\n")
        for r in fix_candidates:
            f.write(f"| {r['keys'][0]} | {r['impressions']} | {r['ctr']*100:.2f}% | {r['position']:.1f} |\n")

        f.write("\n## Top 20 pages by clicks\n\n")
        f.write("| Page | Clicks | Impressions | CTR | Position |\n|---|---|---|---|---|\n")
        for r in top_pages:
            f.write(f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.2f}% | {r['position']:.1f} |\n")

    print(f"GSC: {len(queries)} queries, {len(pages)} pages → {out_dir}/{today}_*.csv + summary.md")


if __name__ == "__main__":
    main()
