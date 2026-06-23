#!/usr/bin/env python3
"""Pull GA4 sessions, sources, landing pages, daily series. CSVs + markdown summary into research/ga4/."""
import os
import csv
import argparse
from datetime import date, timedelta
from pathlib import Path
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, OrderBy
)
from auth import get_credentials


def run_report(client, property_id, start, end, dimensions, metrics, limit=500):
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=metrics[0]), desc=True)],
        limit=limit,
    )
    return client.run_report(req)


def report_to_rows(report):
    headers = [d.name for d in report.dimension_headers] + [m.name for m in report.metric_headers]
    rows = [
        [d.value for d in r.dimension_values] + [m.value for m in r.metric_values]
        for r in report.rows
    ]
    return headers, rows


def write_csv(path: Path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=28)
    parser.add_argument("--out", default="research/ga4")
    args = parser.parse_args()

    property_id = os.environ["GA4_PROPERTY_ID"]
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=args.days)
    out_dir = Path(args.out)
    today = date.today().isoformat()

    creds = get_credentials()
    client = BetaAnalyticsDataClient(credentials=creds)

    sources = run_report(
        client, property_id, start.isoformat(), end.isoformat(),
        ["sessionSource", "sessionMedium"],
        ["sessions", "engagedSessions", "conversions", "totalUsers"],
    )
    s_headers, s_rows = report_to_rows(sources)
    write_csv(out_dir / f"{today}_sources.csv", s_headers, s_rows)

    landing = run_report(
        client, property_id, start.isoformat(), end.isoformat(),
        ["landingPage"],
        ["sessions", "engagedSessions", "conversions", "averageSessionDuration"],
    )
    l_headers, l_rows = report_to_rows(landing)
    write_csv(out_dir / f"{today}_landing_pages.csv", l_headers, l_rows)

    overview = run_report(
        client, property_id, start.isoformat(), end.isoformat(),
        ["date"],
        ["sessions", "engagedSessions", "totalUsers", "newUsers", "conversions"],
        limit=400,
    )
    o_headers, o_rows = report_to_rows(overview)
    write_csv(out_dir / f"{today}_daily.csv", o_headers, o_rows)

    total_sessions = sum(int(r[1]) for r in o_rows)
    total_engaged = sum(int(r[2]) for r in o_rows)
    total_users = sum(int(r[3]) for r in o_rows)
    total_new = sum(int(r[4]) for r in o_rows)
    total_conv = sum(float(r[5]) for r in o_rows)
    engagement_rate = (total_engaged / total_sessions * 100) if total_sessions else 0

    summary = out_dir / f"{today}_summary.md"
    with open(summary, "w") as f:
        f.write(f"# GA4 Summary — {today}\n\n")
        f.write(f"- Property: `{property_id}` (Talkadot Marketing GA4)\n")
        f.write(f"- Window: {start} → {end} ({args.days} days)\n")
        f.write(f"- Sessions: **{total_sessions}**\n")
        f.write(f"- Engaged sessions: **{total_engaged}** ({engagement_rate:.1f}%)\n")
        f.write(f"- Users: **{total_users}** (new: {total_new})\n")
        f.write(f"- Conversions: **{total_conv:.0f}**\n\n")

        f.write("## Top 15 source / medium by sessions\n\n")
        f.write("| Source | Medium | Sessions | Engaged | Conversions | Users |\n|---|---|---|---|---|---|\n")
        for r in s_rows[:15]:
            f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |\n")

        f.write("\n## Top 20 landing pages by sessions\n\n")
        f.write("| Landing page | Sessions | Engaged | Conversions | Avg duration (s) |\n|---|---|---|---|---|\n")
        for r in l_rows[:20]:
            try:
                dur = f"{float(r[4]):.1f}"
            except ValueError:
                dur = r[4]
            f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {dur} |\n")

    print(f"GA4: sources, landing pages, daily → {out_dir}/{today}_*.csv + summary.md")


if __name__ == "__main__":
    main()
