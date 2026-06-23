# YouTube Data API — setup (one-time)

The youtube-* research skills need a free YouTube Data API v3 key.

## Get the key

1. Go to https://console.cloud.google.com → create a project (or pick one).
2. **APIs & Services → Library → search "YouTube Data API v3" → Enable.**
3. **APIs & Services → Credentials → Create Credentials → API key.** Copy it.
4. (Optional but smart) restrict the key to "YouTube Data API v3" only.

## Store it

Either export it in your shell, or put it in a gitignored env file the engine auto-loads:

```bash
mkdir -p ~/.config/youtube-ops
printf 'YOUTUBE_API_KEY=YOUR_KEY_HERE\n' > ~/.config/youtube-ops/.env
chmod 600 ~/.config/youtube-ops/.env
```

The key lives in `~/.config/` (per-operator), NOT in the repo — never commit it.

## Verify

```bash
python3 scripts/youtube/yt_api.py search --query "ai marketing" --max 3
```

You should see three video IDs. If you get a quota error, the default is 10,000 units/day
(one `research` run ≈ 100 + ~3 per channel) — it resets at midnight Pacific.

## What the key does and doesn't unlock

- **Does:** public data on ANY video/channel — views, likes, comments, publish date,
  channel subs, and the recent-uploads median used for outlier multiples. This is all the
  competitor research and idea validation need.
- **Doesn't:** YOUR private analytics — CTR, average view duration, the retention curve.
  Those need the YouTube **Analytics** API (OAuth), which `youtube-analytics-retro` handles
  via a Studio CSV export for v1 (no OAuth required).
