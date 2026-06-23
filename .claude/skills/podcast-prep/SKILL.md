---
name: podcast-prep
description: "Research a podcast guest and generate a complete interview prep package - guest bio, topic themes, questions, screen share ideas, and tension points. Provide guest name, company URL, and any context."
argument-hint: '"Guest Name" "company-url.com" [optional context or notes]'
allowed-tools: Agent, Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
user-invocable: true
---

# Podcast Prep: Research Any Guest and Generate Interview Package

Take a guest name, company URL, and optional context. Research the guest deeply, then produce a structured interview prep document with introduction, topic themes, questions, screen share ideas, and strategic angles.

## CRITICAL: Parse User Input

Before doing anything, extract:

1. **GUEST_NAME**: Full name of the podcast guest
2. **COMPANY_URL**: Their company's website URL
3. **CONTEXT**: Any additional info the user provides (role, topic focus, landing page copy, etc.)

If any of these are missing, ask the user before proceeding.

## Step 1: Research the Guest (use strategy-planner agent)

Launch a research agent to gather:

### Person Research
- **Career path**: Previous roles, companies, education
- **LinkedIn presence**: Content themes, posting frequency, recent posts
- **Twitter/X**: Handle, recent takes, contrarian positions
- **Podcast appearances**: Previous interviews (titles, topics, hosts)
- **Blog posts / writing**: Published articles, Medium, company blog
- **Public opinions**: Strong positions, contrarian takes, frameworks they use
- **Credibility markers**: Specific data points, research they cite, results they share

### Company Research
- **Stage**: Funding raised, investors, team size, ARR if public
- **Product**: What it does NOW (not what it used to do - check for pivots)
- **Positioning**: How they describe themselves on the website
- **Customers**: Named case studies, testimonials, logos
- **Competitors**: Who they compete with, how they differentiate
- **Content**: Blog themes, podcast, YouTube, resources
- **Recent news**: Product launches, funding, pivots, press

### Pivot/Evolution Check
- Has the company changed its positioning or product focus?
- What did they used to do vs. what they do now?
- What drove the change? (This is often the best interview content)

## Step 2: Identify Strategic Angles

Before writing questions, analyze the research for:

### Overlap with the client's worldview
- Where does the guest's thesis align with the client's? (systems thinking, AI, visibility, etc.)
- Where does it diverge? (Different channel focus, different buyer stage, different methodology)
- What is the productive tension between the two worldviews?

### The Guest's Through-Line
- What is the consistent thread across their career and company evolution?
- What problem have they been solving in different ways?

### What's Under-Covered
- What has this guest NOT been asked about in previous podcasts?
- What is their newest thinking that hasn't been explored publicly yet?

### Audience Value
- What can a Series A-B SaaS founder learn from this guest?
- What specific, actionable takeaway should the listener walk away with?

## Step 3: Generate Interview Prep Package

Produce exactly this structure:

### Guest Introduction (ready to read on-air)
- 3-5 sentences. Cover: who they are, what they built, why it matters, one surprising fact.
- Written in Gen's voice - direct, credible, no fluff.
- Include the company's current positioning (not old positioning).

### 5 Topic Themes
For each theme, provide:

1. **Theme Title** (bold, descriptive - not generic)
2. **Why this matters** (2-3 sentences connecting this to the audience and to the client's worldview)
3. **3 Questions** (specific, non-generic, designed to surface insight rather than rehearsed answers)
4. **Screen Share Idea** (what to show on screen during this segment - a dashboard, a comparison, a live demo, data)

### Theme Design Rules
- Theme 1 should be the guest's origin story or pivot story (most engaging for cold audience)
- Theme 2-3 should be their core thesis and how it works in practice
- Theme 4 should be the tension point between their worldview and yours (this creates the best content)
- Theme 5 should be the meta-story or business-building angle (relatable to founder audience)

### Question Writing Rules
- No yes/no questions
- No "tell me about..." (too vague, lets guest give rehearsed answer)
- Lead with a specific claim or data point that forces a reaction
- Include at least 2 questions that reference the guest's own words/data back to them
- Include at least 1 question that creates productive disagreement
- Each question should be something the guest has NOT been asked on previous podcasts

### Screen Share Rules
- Every theme gets a screen share idea
- Screen shares should make abstract concepts visual
- Best types: live product demo, before/after comparison, data dashboard, side-by-side search results
- Include enough detail that the guest can prepare it in advance

## Step 4: Generate Bonus Elements

### Spicy Questions (2-3)
Questions that are provocative but fair. The kind that make the guest pause and give a real answer instead of a rehearsed one.

### Closing Question
One question to end the interview that gives the guest a chance to leave the audience with something memorable. Not "where can people find you" - something substantive.

### Potential Clip Moments
Identify 2-3 question/topic combinations most likely to produce strong short-form clips (bold claims, surprising data, contrarian takes, emotional reactions).

## Step 5: Save Output

Save the complete prep package to:
`clients/{client_slug}/production/podcast/{YYYY-MM-DD}_{guest-slug}_prep.md`

If the directory doesn't exist, create it.

## Output Format

```markdown
# Podcast Prep: {Guest Name}, {Title} at {Company}
Generated: {date}

---

## Guest Introduction (read on-air)

{3-5 sentence introduction}

---

## Research Summary

**Background:** {2-3 sentences on career path}
**Company:** {Company} - {what it does, stage, key metrics}
**Previous podcasts:** {list 3-5 most relevant appearances}
**Key public positions:** {3-5 bullet points of their strongest takes}

---

## Theme 1: {Theme Title}

**Why this matters:** {2-3 sentences}

**Questions:**
1. {Question 1}
2. {Question 2}
3. {Question 3}

**Screen share:** {What to show and why}

---

## Theme 2: {Theme Title}

**Why this matters:** {2-3 sentences}

**Questions:**
1. {Question 1}
2. {Question 2}
3. {Question 3}

**Screen share:** {What to show and why}

---

## Theme 3: {Theme Title}

{Same structure}

---

## Theme 4: {Theme Title}

{Same structure}

---

## Theme 5: {Theme Title}

{Same structure}

---

## Spicy Questions

1. {Provocative but fair question}
2. {Provocative but fair question}
3. {Provocative but fair question}

---

## Closing Question

{One substantive closing question}

---

## Potential Clip Moments

1. **{Topic}** - {Why this will produce a strong clip}
2. **{Topic}** - {Why this will produce a strong clip}
3. **{Topic}** - {Why this will produce a strong clip}
```

## Quality Checks

Before presenting output, verify:
- [ ] Introduction is in Gen's voice - direct, no fluff, no corporate language
- [ ] All 5 themes have questions, rationale, AND screen share ideas
- [ ] No generic questions ("tell me about your journey")
- [ ] At least 2 questions reference the guest's own words or data
- [ ] At least 1 question creates productive tension with the client's worldview
- [ ] Questions are specific enough that the guest can't give a rehearsed answer
- [ ] Screen share ideas are concrete and preparable
- [ ] Company description reflects CURRENT positioning, not old/deprecated positioning
- [ ] No banned phrases from output style
- [ ] Spicy questions are provocative but respectful
- [ ] The closing question is substantive, not logistical

## Example Usage

```
# Full prep with context
/podcast-prep "Parthi Loganathan" "letterdrop.com" "CEO, pivoted from SEO to sales intelligence, here's their landing page copy: ..."

# Minimal input
/podcast-prep "Jane Smith" "acme.com"

# With topic focus
/podcast-prep "John Doe" "signalfire.com" "Want to focus on AI search and how VCs evaluate visibility"
```
