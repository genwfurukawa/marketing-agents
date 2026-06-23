#!/usr/bin/env python3
"""YouTube Data API v3 engine for the youtube-* research skills.

The thing WebSearch can't give you: real view counts, view velocity, and — most
importantly — OUTLIER MULTIPLES (a video's views divided by its channel's recent median).
Outlier multiple is the single best signal for "this idea/packaging overperformed," which
is what competitor research and idea validation are actually after.

Key: set YOUTUBE_API_KEY in the environment or in ~/.config/youtube-ops/.env.
Get one free at https://console.cloud.google.com → enable "YouTube Data API v3" → API key.

Subcommands:
  search   --query "kw" [--max 50] [--order viewCount|relevance|date] [--days N] [--region US]
  videos   --ids id1,id2,...
  research --query "kw" [--max 40] [--days N] --out research/youtube/<kw>/
           (search → enrich with stats → channel baselines → outlier multiples → JSON+CSV)

Quota notes: search.list costs 100 units; videos/channels/playlistItems cost 1 each.
Default daily quota is 10,000 units. One `research` run ≈ 100 + ~3/channel units.
"""
import argparse
import csv
import json
import os
import statistics
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://www.googleapis.com/youtube/v3"
ENV_PATH = Path.home() / ".config" / "youtube-ops" / ".env"


def load_key():
    if not os.environ.get("YOUTUBE_API_KEY") and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    key = os.environ.get("YOUTUBE_API_KEY", "")
    if not key:
        sys.exit("ERROR: YOUTUBE_API_KEY not set. See youtube-competitor-research/setup.md.")
    return key


def api_get(endpoint, params):
    params = {k: v for k, v in params.items() if v is not None}
    params["key"] = load_key()
    url = f"{BASE}/{endpoint}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        if e.code == 403 and "quota" in body.lower():
            sys.exit("ERROR: YouTube API quota exceeded for today. Try again tomorrow or "
                     "request a higher quota in Google Cloud.")
        sys.exit(f"ERROR {e.code} on {endpoint}: {body[:400]}")


def _iso_n_days_ago(days):
    if not days:
        return None
    return (datetime.now(timezone.utc) - timedelta(days=int(days))).strftime("%Y-%m-%dT%H:%M:%SZ")


def search(query, max_results=50, order="viewCount", days=None, region=None):
    """Return up to max_results video ids for a keyword."""
    ids, token, got = [], None, 0
    while got < max_results:
        data = api_get("search", {
            "part": "snippet", "q": query, "type": "video",
            "maxResults": min(50, max_results - got), "order": order,
            "publishedAfter": _iso_n_days_ago(days), "regionCode": region,
            "relevanceLanguage": "en", "pageToken": token,
        })
        ids += [it["id"]["videoId"] for it in data.get("items", []) if it["id"].get("videoId")]
        got = len(ids)
        token = data.get("nextPageToken")
        if not token:
            break
    return ids[:max_results]


def videos(ids):
    """Hydrate video ids with stats + snippet + duration (batched 50/call)."""
    out = []
    for i in range(0, len(ids), 50):
        data = api_get("videos", {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(ids[i:i + 50]),
        })
        for it in data.get("items", []):
            st, sn = it.get("statistics", {}), it.get("snippet", {})
            out.append({
                "video_id": it["id"],
                "title": sn.get("title"),
                "channel": sn.get("channelTitle"),
                "channel_id": sn.get("channelId"),
                "published": sn.get("publishedAt"),
                "views": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "comments": int(st.get("commentCount", 0)),
                "duration": it.get("contentDetails", {}).get("duration"),
                "thumbnail": (sn.get("thumbnails", {}).get("high") or {}).get("url"),
            })
    return out


def channel_baseline(channel_id, cache):
    """Median views of a channel's ~25 most recent uploads. ~3 quota units, cached."""
    if channel_id in cache:
        return cache[channel_id]
    ch = api_get("channels", {"part": "contentDetails,statistics", "id": channel_id})
    items = ch.get("items", [])
    if not items:
        cache[channel_id] = {"median": None, "subs": None}
        return cache[channel_id]
    subs = int(items[0].get("statistics", {}).get("subscriberCount", 0)) or None
    uploads = items[0]["contentDetails"]["relatedPlaylists"].get("uploads")
    vids = []
    if uploads:
        pl = api_get("playlistItems", {"part": "contentDetails", "playlistId": uploads, "maxResults": 25})
        vids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]
    median = None
    if vids:
        views = [v["views"] for v in videos(vids) if v["views"] > 0]
        median = statistics.median(views) if views else None
    cache[channel_id] = {"median": median, "subs": subs}
    return cache[channel_id]


def research(query, max_results, days, region, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Searching '{query}' (max {max_results}, order=viewCount"
          f"{', last %sd' % days if days else ''})...")
    ids = search(query, max_results, "viewCount", days, region)
    if not ids:
        sys.exit("No results.")
    rows = videos(ids)
    print(f"Hydrating {len(rows)} videos + channel baselines...")

    cache = {}
    now = datetime.now(timezone.utc)
    for r in rows:
        base = channel_baseline(r["channel_id"], cache)
        r["channel_subs"] = base["subs"]
        r["channel_median_views"] = base["median"]
        r["outlier_multiple"] = round(r["views"] / base["median"], 2) if base["median"] else None
        # Engagement rate exposes paid distribution: a high-view video with near-zero
        # likes+comments was served as an ad, not earned organically — so its outlier
        # multiple is bought, not a packaging/idea signal. Flag and demote those.
        r["engagement_rate"] = round((r["likes"] + r["comments"]) / r["views"] * 100, 3) if r["views"] else None
        r["likely_paid"] = bool(r["views"] >= 10000 and r["engagement_rate"] is not None
                                and r["engagement_rate"] < 0.5)
        try:
            pub = datetime.fromisoformat(r["published"].replace("Z", "+00:00"))
            r["age_days"] = max(1, (now - pub).days)
            r["views_per_day"] = round(r["views"] / r["age_days"])
        except Exception:
            r["age_days"], r["views_per_day"] = None, None

    # Sort organic outliers to the top; likely-paid sink regardless of raw multiple.
    rows.sort(key=lambda r: (not r["likely_paid"], r["outlier_multiple"] or 0), reverse=True)

    (out_dir / "competitors.json").write_text(json.dumps(
        {"query": query, "pulled": now.isoformat(), "count": len(rows), "videos": rows}, indent=2))
    with open(out_dir / "competitors.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "outlier_multiple", "engagement_rate", "likely_paid", "views_per_day",
            "views", "channel_subs", "channel_median_views", "age_days",
            "channel", "title", "video_id"])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in w.fieldnames})

    paid = sum(1 for r in rows if r["likely_paid"])
    print(f"\nTop outliers for '{query}' (organic first; {paid} flagged likely-paid):")
    print(f"{'OUT×':>7} {'ENG%':>6} {'VPD':>7} {'VIEWS':>11}  CHANNEL · TITLE")
    for r in rows[:15]:
        ox = f"{r['outlier_multiple']}x" if r["outlier_multiple"] else "  -"
        eng = f"{r['engagement_rate']:.2f}" if r["engagement_rate"] is not None else "-"
        flag = "  ⚠paid" if r["likely_paid"] else ""
        print(f"{ox:>7} {eng:>6} {str(r['views_per_day'] or '-'):>7} {r['views']:>11,}  "
              f"{(r['channel'] or '?')[:16]:16} · {(r['title'] or '')[:40]}{flag}")
    print(f"\nWrote {out_dir}/competitors.json + .csv")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.add_argument("--query", required=True)
    s.add_argument("--max", type=int, default=50); s.add_argument("--order", default="viewCount")
    s.add_argument("--days", type=int); s.add_argument("--region")

    v = sub.add_parser("videos"); v.add_argument("--ids", required=True)

    r = sub.add_parser("research"); r.add_argument("--query", required=True)
    r.add_argument("--max", type=int, default=40); r.add_argument("--days", type=int)
    r.add_argument("--region"); r.add_argument("--out", required=True)

    a = p.parse_args()
    if a.cmd == "search":
        print(json.dumps(search(a.query, a.max, a.order, a.days, a.region), indent=2))
    elif a.cmd == "videos":
        print(json.dumps(videos(a.ids.split(",")), indent=2))
    elif a.cmd == "research":
        research(a.query, a.max, a.days, a.region, a.out)


if __name__ == "__main__":
    main()
