---
description: Distribution orchestration - schedule QA-approved content across channels, create publish packages, log distribution
argument-hint: [--client client-slug] [--sprint-dir path/to/sprint/] [--dry-run]
allowed-tools: Task, Read, Write, Glob, Grep, WebFetch
---

# Distribute - Cross-Channel Publishing Orchestration

You orchestrate the distribution of QA-approved content across all channels. You generate platform-specific publish packages (copy-paste ready), schedule content across the week, and log everything for the retro phase.

This is the marketing equivalent of G-Stack's `/ship` + `/land-and-deploy` - getting the work from "approved" to "live and verified."

## Prerequisites

1. Content has passed QA (check `qa_report.md` for PASS status)
2. Client context loaded from `clients_registry.json`
3. Config loaded: `clients/{client}/config.yaml` for channel frequency targets and pillar balance

If QA report shows FAIL, STOP and report: "QA has blocking issues. Fix those first with `/content-qa`."

## Input

- `--sprint-dir path/to/sprint/` - Distribute all QA-approved content from a sprint
- `--client client-slug` - Resolve client workspace path
- `--dry-run` - Generate packages and schedule but don't log as distributed

## Step 1: Load QA-Approved Drafts

Read `qa_report.md` from the sprint directory. Collect all drafts with PASS or PASS WITH WARNINGS status.

Read each draft from `drafts/` directory and its frontmatter metadata.

## Step 2: Generate Distribution Schedule

Create a distribution calendar for the week based on:

**Frequency targets** (from clients/{client}/config.yaml):
- LinkedIn: 2-3x per week
- Blog/AEO: 2x per month
- YouTube: 1x per week
- Email/Newsletter: 1x per week

**Pillar balance targets:**
- AEO: 40% of content
- AI + Marketing: 25%
- Claude Code: 20%
- B2B SaaS: 15%

**Scheduling rules:**
- LinkedIn: Tuesday, Wednesday, Thursday mornings (8-10am ET)
- Blog: Monday or Wednesday
- YouTube: Thursday or Friday
- Email: Tuesday or Thursday morning
- Never stack 2 pieces on the same channel on the same day
- Space LinkedIn posts at least 1 day apart

Output schedule as a table:

```markdown
## Distribution Schedule: {sprint_id}

| Day | Time (ET) | Channel | Piece | Pillar |
|-----|-----------|---------|-------|--------|
| Tue | 9:00 AM | LinkedIn | {title} | AEO |
| Tue | 10:00 AM | Email | {title} | AI+Marketing |
| Wed | 9:00 AM | LinkedIn | {title} | Claude Code |
| Thu | 9:00 AM | LinkedIn | {title} | B2B SaaS |
| Thu | 2:00 PM | YouTube | {title} | AEO |
| Fri | 9:00 AM | Blog | {title} | AEO |
```

## Step 3: Generate Platform-Specific Publish Packages

For each content piece, create a copy-paste-ready publish package.

### LinkedIn Publish Package

```markdown
## LinkedIn Publish Package: {slug}

**Scheduled:** {day}, {time} ET
**Pillar:** {pillar}

### Post Copy (copy-paste ready)
---
{final post text - no frontmatter, no markdown headers, just the raw post}
---

### Hashtags
{tag1} {tag2} {tag3}

### Image
{If applicable: image file path or generation instructions}

### Tracking
- UTM link (if applicable): {url}?utm_source=linkedin&utm_medium=organic&utm_campaign={sprint_id}
```

### Blog Publish Package

```markdown
## Blog Publish Package: {slug}

**Scheduled:** {day}
**Pillar:** {pillar}

### Meta
- **Title tag:** {50-60 chars}
- **Meta description:** {150-160 chars}
- **URL slug:** /{slug}
- **Category:** {pillar}
- **Tags:** {tag1}, {tag2}, {tag3}

### Schema Markup (JSON-LD)
```json
{schema markup block}
```

### Content (CMS-ready)
---
{Full content with proper heading hierarchy}
---

### Internal linking opportunities
- Link to: {related existing page}
- Link from: {existing page that should link here}
```

### Email Publish Package

```markdown
## Email Publish Package: {slug}

**Scheduled:** {day}, {time} ET
**List segment:** {target segment}

### Subject line
{subject line - max 50 chars}

### Preview text
{preview text - max 90 chars}

### Body (copy-paste ready)
---
{email body - 250-400 words}
---

### CTA
- **Text:** {CTA text}
- **URL:** {url}?utm_source=email&utm_medium=newsletter&utm_campaign={sprint_id}

### Send settings
- From: {sender name}
- Reply-to: {email}
```

### YouTube Publish Package

```markdown
## YouTube Publish Package: {slug}

**Scheduled:** {day}, {time} ET

### Title (pick one)
1. {option 1 - max 70 chars}
2. {option 2}
3. {option 3}

### Description
{Full description with chapters/timestamps}

### Tags
{comma-separated tags}

### Thumbnail
{Thumbnail concept or file path}

### Cards & End Screens
- Card at {timestamp}: {linked video/playlist}
- End screen: {subscribe + video suggestion}

### Pinned Comment
{First comment to pin}
```

## Step 4: Create Notion Content Calendar Entries

For each content piece, create an entry in the Notion Content Calendar database via MCP:

- Title: {content title}
- Channel: {LinkedIn/Blog/YouTube/Email}
- Pillar: {content pillar}
- Status: "Scheduled"
- Publish date: {scheduled date}
- Sprint: {sprint_id}
- Draft link: {path to draft file}

If Notion MCP is unavailable, log this as a manual action item.

## Step 5: Save to Client Workspace

Copy final publish-ready content to the client workspace output directories:

| Format | Destination |
|--------|------------|
| LinkedIn | `{client_root}/04_content_engine/linkedin/final/{date}_{slug}.md` |
| Blog | `{client_root}/04_content_engine/blogs/final/{slug}.md` |
| Email | `{client_root}/04_content_engine/newsletters/final/{date}_{slug}.md` |
| YouTube | `{client_root}/04_content_engine/youtube/final/{slug}/` |
| Carousel | `{client_root}/04_content_engine/carousels/final/{date}_{slug}.md` |

## Step 6: Log Distribution

Write `distribution_log.md` to the sprint directory:

```markdown
# Distribution Log: {sprint_id}

**Client:** {client_slug}
**Generated:** {timestamp}
**Mode:** {dry-run or live}

## Schedule

| # | Day | Time | Channel | Title | Pillar | Status |
|---|-----|------|---------|-------|--------|--------|
| 1 | Tue 9am | LinkedIn | {title} | AEO | Scheduled |
| 2 | Wed 9am | LinkedIn | {title} | Claude Code | Scheduled |
| ... | ... | ... | ... | ... | ... |

## Pillar Balance

| Pillar | Target | Actual | Status |
|--------|--------|--------|--------|
| AEO | 40% | {pct}% | {on track / over / under} |
| AI + Marketing | 25% | {pct}% | {status} |
| Claude Code | 20% | {pct}% | {status} |
| B2B SaaS | 15% | {pct}% | {status} |

## Publish Packages

### 1. {title}
- Channel: {channel}
- File: {path to final file}
- Notion entry: {created / skipped}
- UTM: {tracking link}

### 2. {title}
...

## Post-Publish Verification Checklist

After publishing, verify each piece:
- [ ] {title} - Published on {channel} at {url}
- [ ] {title} - Published on {channel} at {url}
...

## Notes
{Any scheduling conflicts, pillar imbalances, or manual actions needed}
```

## Step 7: Post-Publish Verification (if not dry-run)

After the distribution window, the user can run `/sprint distribute --verify`:

For each published piece:
1. WebFetch the published URL
2. Verify content is live and accessible
3. Check that tracking parameters are in place
4. Update distribution_log.md with verification status

## Dry Run Mode

With `--dry-run`:
- Generate all packages and schedules
- Do NOT create Notion entries
- Do NOT copy to client final directories
- Log as "DRY RUN" in distribution_log.md
- Present everything for approval first

## Rules

1. Never distribute content that hasn't passed QA
2. Always generate copy-paste-ready packages (zero editing needed to publish)
3. Always include UTM parameters on trackable links
4. Respect channel frequency limits from clients/{client}/config.yaml
5. Balance pillars as close to target percentages as possible
6. Log everything - the retro phase depends on complete distribution data
7. Default to dry-run if uncertain - better to preview than publish wrong
8. Save all final content to client workspace output directories
