# YouTube Content System (methodology)

## Overview

This YouTube content system helps you establish thought leadership in the AEO (Answer Engine Optimization) and AI-powered content marketing space by creating SEO-optimized tutorials, tool walkthroughs, build-in-public content, and news analysis.

## Target Audience

**Primary:** Marketing Directors at B2B SaaS companies ($5M-$50M revenue)
- See full ICP: `/{client_root}/LIGHTHOUSE_CLIENT_PROFILE.md`

## Content Strategy

### Goals
1. **Thought Leadership:** Position as THE go-to expert for AEO and AI content marketing
2. **Lead Generation:** Attract discovery calls from Marketing Directors
3. **Community Building:** Create engaged audience of marketing practitioners

### Publishing Schedule
**2 videos per week:**
- **Main Video (Monday):** 10-15 min tutorial/walkthrough
- **Supplementary (Thursday):** 5-8 min build-in-public, news analysis, or quick tutorial

### Content Mix (All 4 Formats)

#### 1. Tactical Tutorials (40% of content)
**"How to implement X"**
- Step-by-step AEO strategies
- AI search optimization techniques
- Content workflow setups
- Examples: "How to Optimize Content for Perplexity AI", "AEO Audit Checklist Walkthrough"

#### 2. Tool Walkthroughs (30% of content)
**"How I use Claude Code/AirOps/Airtable"**
- Screen recordings of actual workflows
- Setup guides
- Integration tutorials
- Examples: "My AirOps + Airtable Content Workflow", "How I Use Claude Code for Content Briefs"

#### 3. Build in Public (20% of content)
**"Creating X in real-time"**
- Building workflows live
- Testing new strategies
- Problem-solving sessions
- Examples: "Building an AEO Content Brief (Unedited)", "Testing 5 AI Search Engines for Citations"

#### 4. News/Trend Analysis (10% of content)
**"What X means for marketers"**
- AI search engine updates
- Google algorithm changes
- Industry trend breakdowns
- Examples: "Google AI Overviews Update: What Changed", "ChatGPT Search Impact on Content Strategy"

## Discovery Strategy

### SEO-First Approach
**Primary Focus:** Rank for "how to" searches that Marketing Directors are actively searching for

**Target Search Queries (from AEO questions):**
- "how to optimize for Perplexity AI"
- "what is AEO"
- "how to measure content ROI"
- "AI content workflow"
- "ChatGPT SEO optimization"

**SEO Tactics:**
- Front-load primary keyword in title (first 40 characters)
- Detailed descriptions with timestamps
- Long-tail keyword tags
- Answer specific questions in video
- Create playlists around topic clusters

## Using This System

### Quick Commands

Run the main `/youtube` skill to orchestrate all sub-agents:

```bash
# Generate video ideas for the week
/youtube ideas "AEO tutorial for marketing directors"

# Write a script for a specific topic
/youtube script long-form "How to Set Up AirOps for AEO Content Production"

# Design thumbnail concepts
/youtube thumbnail "shocked face looking at AI citation dashboard"

# Optimize metadata for SEO
/youtube seo "How to Optimize Your Content for Perplexity AI (Step-by-Step)"

# Full end-to-end workflow
/youtube full "Building an AEO Content Brief with Claude Code"
```

### Context Sources (Automatically Pulled)

The YouTube agents will automatically reference:

1. **Client ICP:** `/{client_root}/LIGHTHOUSE_CLIENT_PROFILE.md`
   - Pain points Marketing Directors face
   - Goals and desired outcomes
   - Content preferences and tone

2. **Merged Atoms:** `/03_insight_layer/seeds/merged_atoms.json`
   - Your unique insights and frameworks
   - Personal experiences and case studies
   - Proprietary methodologies

3. **AEO Questions:** `/02_research/ao_search/aeo_questions.json`
   - What people are searching for
   - Question-based content opportunities
   - Search intent data

4. **Competitive Intelligence:** `/02_research/competitors/competitive_atoms.json`
   - What competitors are covering
   - Content gaps and opportunities
   - Differentiation angles

## Output Layout

Agent outputs land in the active client's production tree under a consistent folder structure:

```
clients/{slug}/production/youtube/
├── ideas/              ← Strategy-agent idea lists (one .md per session)
├── scripts/
│   ├── long-form/      ← 10–15 min tutorial scripts
│   ├── shorts/         ← 60-second vertical scripts
│   └── green-screen/   ← News/reaction scripts
├── thumbnails/         ← Thumbnail concepts (3 variants per video, .json + .png)
└── seo/                ← Publish packages: titles, descriptions, tags, chapters
```

Create the subfolders on demand the first time each agent runs.

## Weekly Workflow

### Monday (Main Video - Tactical Tutorial)

1. **Ideation (15 min)**
   - Run `/youtube ideas "tactical AEO tutorial"`
   - Review 10-15 ideas ranked by search potential
   - Select topic with highest SEO opportunity score

2. **Script Writing (45-60 min)**
   - Run `/youtube script long-form "[selected topic]"`
   - Review script for:
     - Hook strength (first 8 seconds)
     - Tactical value (can they implement it?)
     - SEO keyword integration
   - Add personal anecdotes from your experience

3. **Thumbnail Design (20 min)**
   - Run `/youtube thumbnail "[concept from script]"`
   - Select Concept A for launch (test B/C if CTR underperforms)

4. **SEO Optimization (15 min)**
   - Run `/youtube seo "[video title]"`
   - Review title variations (use SEO-optimized option)
   - Copy description, tags, timestamps

5. **Film & Edit (2-3 hours)**
   - Film using script as guide (allow natural delivery)
   - Edit following retention cues in script
   - Add B-roll based on script suggestions

6. **Publish & Monitor (10 min)**
   - Upload with metadata
   - Post pinned comment immediately
   - Share on LinkedIn with tease
   - Monitor first 24-hour CTR (target: 8%+)

### Thursday (Supplementary Video)

**Option A: Build in Public**
- Screen record building a workflow
- Minimal editing
- Post "raw" version (authentic)

**Option B: News Analysis**
- React to AI search update
- 5-7 min breakdown
- Quick turnaround (same day as news)

**Option C: Quick Tutorial**
- Single tactic or tool tip
- 5-8 min focused tutorial
- Leverage script from failed sections of longer videos

## Content Calendar Template

See: `{client_root}/workflows/youtube/content_calendar.md`

## Success Metrics

### Track These (YouTube Studio Analytics)

**Traffic Sources:**
- YouTube search: 40-60% (SEO-first strategy)
- Suggested videos: 20-30%
- External (LinkedIn shares): 10-20%

**Engagement:**
- CTR: 8-12% target (10%+ is excellent)
- Average View Duration: 50%+ (8+ min on 15-min video)
- Engagement rate: 4%+ (likes, comments, shares)

**Growth:**
- Subscribers: 100-200/month (quality over quantity)
- Watch time: 10,000+ hours annually (monetization threshold)

**SEO Performance:**
- Top 10 ranking for target keywords within 30 days
- 5+ target keywords in top 3 within 90 days

**Lead Generation (Most Important):**
- Discovery calls booked from YouTube: 2-5/month
- Comment engagement from Marketing Directors
- LinkedIn connection requests mentioning video

## Content Ideation Framework

### Filter Every Idea Through:

1. **ICP Alignment (Critical)**
   - Does this solve a Marketing Director pain point?
   - Would they actually search for this?
   - Is it tactical enough to implement?

2. **Search Potential (SEO-First)**
   - Is there search volume for this topic?
   - Can we rank in top 10 within 30 days?
   - Are there long-tail keyword opportunities?

3. **Differentiation (Thought Leadership)**
   - What's our unique angle vs. competitors?
   - Does this showcase expertise in AEO?
   - Will this position me as an authority?

4. **Production Feasibility**
   - Can we produce this with available tools/time?
   - Is it repeatable (system, not one-off)?
   - Does it fit our 2 videos/week cadence?

**If 3+ YES → Create this content**
**If 1-2 YES → Refine the angle**
**If 0 YES → Skip it**

## Thumbnail Psychology for B2B Audience

Unlike consumer content, our B2B Marketing Director audience responds to:

**What Works:**
- Professional but approachable facial expressions
- Clear value signals ("5 Steps", "Complete Guide")
- Tool screenshots/dashboards (builds credibility)
- Before/after data visualizations
- Confident, expert posture

**What Doesn't Work:**
- Overly shocked/surprised faces (too consumer-y)
- Clickbait elements (they're savvy, won't fall for it)
- Busy/cluttered designs
- Generic stock photos

**Color Schemes That Perform:**
- Dark blue + bright orange (professional + urgent)
- Black + white + neon green (modern, tech-forward)
- Purple + yellow (differentiated, creative)

## Video Script Formula for Marketing Directors

### Hook (0:00-0:08) - CRITICAL
**Patterns That Work:**
1. **Bold Claim:** "This is the fastest way to optimize for AI search engines"
2. **Pain Point:** "If your traffic is down 20%+, here's why"
3. **Data Hook:** "I analyzed 500 sites for AEO readiness. Only 3% passed."
4. **Contrarian:** "Stop optimizing for Google. Here's what to do instead."

### Body (0:08-10:00)
- **Tactical frameworks** (step 1, 2, 3...)
- **Screen recordings** showing actual tools
- **Data/examples** proving it works
- **Pattern interrupts** every 30-45 seconds

### Conclusion (10:00-12:00)
- Recap key takeaways (3 bullets)
- Strong CTA: "Download the AEO audit checklist (link in description)"
- Next video tease: "Watch this next to learn [related topic]"

## Common Mistakes to Avoid

1. **Theory without tactics** - Marketing Directors need HOW, not just WHY
2. **Generic AI content** - Everyone talks about AI; focus on AEO specifically
3. **No clear CTA** - Every video should drive to lead magnet or call booking
4. **Ignoring SEO** - Can't rely on viral hits; need sustainable search traffic
5. **Inconsistent publishing** - Algorithm rewards consistency; batch if needed

## Tools & Resources

### Filming
- **Camera:** iPhone or webcam (quality matters less than content)
- **Mic:** Rode VideoMic or Shure MV7 (audio is MORE important than video)
- **Lighting:** Ring light or natural window light
- **Screen Recording:** Loom, QuickTime, or OBS

### Editing
- **Beginner:** iMovie, Clipchamp (free, simple)
- **Intermediate:** DaVinci Resolve (free, powerful)
- **Advanced:** Final Cut Pro, Premiere Pro (if budget allows)

### Thumbnails
- **Canva:** Pre-made YouTube thumbnail templates
- **Photoshop:** Full control for custom designs
- **Remove.bg:** Background removal for clean cutouts

### SEO Research
- **TubeBuddy:** Keyword research, tag suggestions
- **VidIQ:** Competitor analysis, trend tracking
- **Google Trends:** Search volume validation

## Next Steps

1. **Run Initial Ideation**
   - `/youtube ideas "AEO tutorials for marketing directors"`
   - Review generated ideas
   - Select top 5 for next month

2. **Create First Video**
   - Start with highest SEO potential idea
   - Run `/youtube full "[topic]"` for complete package
   - Film and publish

3. **Establish Baseline Metrics**
   - Track first 5 videos for CTR, AVD, traffic sources
   - Identify what's working
   - Double down on winners

4. **Iterate Weekly**
   - Use analytics to inform next video topics
   - Test different formats (tutorial vs. build-in-public)
   - Refine thumbnails based on CTR data

---

**Questions? Need help?**

Run `/youtube` commands to generate ideas, scripts, thumbnails, and SEO metadata automatically using the specialized YouTube agents.
