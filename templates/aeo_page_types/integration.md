# Integration Page Template

> Page type designed for AI retrieval on "tools that integrate with {product}" and "{Product A} + {Product B} integration" queries.
> Creates entity co-occurrence signals between products. One of the most powerful and underused AI SEO tactics.

---

## Required Structure

### 1. H1: Title

Format: `{Product A} + {Product B} Integration: {Value Proposition}`

Examples:
- "Slack + Salesforce Integration: Close Deals Without Leaving Chat"
- "Stripe + QuickBooks Integration: Automate Revenue Recognition"

Rules:
- Both product names connected with "+"
- Include what the integration does (not just that it exists)
- Use action-oriented language in the qualifier

### 2. Integration Overview Block (CRITICAL)

**Place immediately after H1. No preamble.**

Template:
```
**{Product A} integrates with {Product B} to {primary value in one sentence}.** This integration {key capability}, saving {ICP role} approximately {time/effort estimate} per {timeframe}. {One sentence on who benefits most.}
```

Rules:
- 40-60 words
- Explain what the integration DOES, not just that it exists
- Include a tangible benefit (time saved, automation gained)
- LLMs extract this when answering "does X integrate with Y?"

### 3. Section: What This Integration Does

H2: `What Does the {Product A} + {Product B} Integration Do?`

Content:
- 3-5 bullet points of specific capabilities
- Each bullet: action verb + what gets synced/automated + outcome
- Be specific about data flow direction

Example:
```
- **Syncs new leads automatically** - When a prospect engages with your content, their profile flows into your CRM without manual entry.
- **Triggers follow-up sequences** - Content engagement signals automatically start outreach workflows.
```

### 4. Section: Setup Steps (HowTo - CRITICAL for schema)

H2: `How to Set Up the {Product A} + {Product B} Integration`

Content:
- Numbered steps (aim for 4-8 steps)
- Each step: clear action + expected result
- Include prerequisites
- Note approximate setup time

Format:
```
**Prerequisites:**
- {Product A} account ({tier} plan or higher)
- {Product B} account with admin access
- Approximately {time} to complete setup

**Step 1: {Action}**
{1-2 sentences explaining what to do and what you'll see}

**Step 2: {Action}**
{1-2 sentences}
```

Rules:
- Steps must be specific enough to follow
- Include which settings screens to navigate to
- Note any permissions required
- This section generates HowTo schema

### 5. Section: Use Case Scenarios

H2: `{Product A} + {Product B} Integration Use Cases`

Content:
- 3-5 specific use cases
- Each use case: H3 heading + scenario + how the integration helps + outcome

Format:
```
### Use Case: {Scenario Name}

**Scenario:** {Who is doing what and why}
**How the integration helps:** {What it automates or connects}
**Result:** {Measurable outcome}
```

### 6. Section: Data Flow

H2: `How Data Flows Between {Product A} and {Product B}`

Content:
- Text description of data flow (since we can't embed images)
- What data moves in each direction
- Sync frequency (real-time, hourly, daily)
- What happens to existing data during setup

### 7. Section: Technical Requirements

H2: `Technical Requirements and Limitations`

Content:
- Supported plans/tiers
- API rate limits if applicable
- Data format requirements
- Known limitations
- Security/compliance notes

### 8. Section: Alternatives

H2: `Alternative Integration Options`

Content:
- Other tools that achieve similar integration
- Zapier/Make workarounds if native integration is limited
- Comparison: native vs third-party integration

### 9. FAQ Section (REQUIRED)

H2: `{Product A} + {Product B} Integration FAQ`

Question patterns:
1. "Does {Product A} integrate with {Product B}?" (yes + what it does)
2. "How do I connect {Product A} to {Product B}?" (setup summary)
3. "Is the {Product A} + {Product B} integration free?" (pricing)
4. "What data syncs between {Product A} and {Product B}?" (data flow)
5. "How long does it take to set up?" (time estimate)
6. "Can I use Zapier instead?" (alternatives)

---

## JSON-LD Schemas Required

### HowTo Schema (for setup steps)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Set Up {Product A} + {Product B} Integration",
  "description": "{Integration overview text}",
  "totalTime": "PT{minutes}M",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "{Step title}",
      "text": "{Step description}"
    }
  ]
}
```

### FAQPage Schema + Article Schema

---

## Quality Checklist

- [ ] Integration overview is 40-60 words and explains what it DOES
- [ ] Setup steps are specific and numbered (4-8 steps)
- [ ] 3-5 use case scenarios with outcomes
- [ ] Data flow direction clearly explained
- [ ] Technical requirements and limitations listed
- [ ] Alternative integration options mentioned
- [ ] FAQ has 5-7 questions
- [ ] Both product names appear consistently throughout
- [ ] HowTo schema generated from setup steps
- [ ] Honest about limitations

---

## Target Metrics

- **Word count**: 1,200-2,000 words
- **Setup steps**: 4-8
- **Use cases**: 3-5
- **FAQ count**: 5-7 questions
- **Refresh cadence**: Quarterly (integration capabilities change)
