# PRD: SuperMarketers Prompt Tracker

Status: public PRD with local-first 0.1 reference implementation. Updated October 7, 2026.

[Run the open-source tracker](../../tools/prompt-tracker/README.md).

## Purpose and user value

Help marketers answer three questions: Are we recommended for the buyers we serve? Which sources and product claims shape those answers? What should we change and test next?

A beginner should be able to clone the SuperMarketers marketing-agents repository, configure their brand and provider keys, run a small buyer-question cohort, inspect the evidence, and create a prioritized action report. The product teaches a repeatable research method alongside providing a usable tracker.

## Scope

Four API routes: OpenAI (dashboard label ChatGPT), Google Gemini, Anthropic Claude, and Perplexity. Actual model IDs, provider and search backend must always accompany the labels. Provider APIs are observations of those routes, not equivalent measurements of their consumer applications. Gemini is not Google AI Overviews. If Gemini is explicitly routed through another provider, record that provider and search backend and keep it as a distinct cohort.

The 0.1 dashboard supports manual Google AI Overviews records, including a successful “No overview” observation. Automated AI Overviews collection is a separate SERP integration roadmap item; it must query and preserve Google Search result data, never infer the Overview from a Gemini answer. A candidate adapter is a SERP provider whose documented response contains an AI Overview element; validate current coverage, location/device support, and per-call cost with a capped pilot before implementation. Manual consumer-UI imports are a separate cohort. No automated CMS publishing, consumer-chat scraping, or automated claims of causal revenue lift. Analytics imports and recurring schedules follow the manual-run MVP.

## Core user journey

1. Create a project: brand aliases, owned domains, competitors, audience, market and language.
2. Add buyer questions in three groups: unbranded Discovery, branded Comparison, and Accuracy/objections. Give each a purpose and version. Start with four prompts across four providers: 16 requests for one repetition. Sixteen prompts across four providers means 64 requests.
3. Preview a run: exact prompt versions, model IDs, search settings, repetitions, maximum requests and budget. Show missing credentials before starting; permit a clearly labeled partial run.
4. Execute fresh independent requests, save raw evidence immediately, retry transient failures, and resume without rerunning successful requests. Never silently substitute a provider or model.
5. Review full answers, final citations and separately retrieved sources. Confirm suggested brand recommendations and fact checks with evidence spans.
6. Inspect dashboard, choose a content action, record what shipped, rerun a matched cohort and export a report.

## MVP components and acceptance criteria

| Component | Requirement | Acceptance |
|---|---|---|
| Project and prompt library | Multiple projects; aliases/domains; groups, tags and immutable prompt versions | An edit creates a new version without changing historical results |
| Provider adapters | Common request/result interface; configurable model; explicit search support and routing | Four configured adapters produce durable records; unavailable accounts return visible failures |
| Run coordinator | Run manifest, request cap, retry/backoff, completion status, resumability | Restart resumes only incomplete requests; partial runs remain inspectable |
| Evidence store | Raw response plus normalized text, citations, retrieved sources, usage and metadata | Every dashboard result opens its original evidence; incomplete output cannot become a completed answer |
| Review workflow | Mention vs recommendation vs comparison preference; evidence span; selected claim checks | Reviewer can correct labels; unknown stays unknown; scorer version and review status are retained |
| Dashboard | Filters by project/group/provider/model/mode/run/date; rates, competitors, source map, stale claims and coverage | Every metric displays numerator/denominator and opens supporting answers |
| Action and experiment log | Target prompts/pages, hypothesis, owner, change, ship date, baseline and follow-up cohort | A report links results to an explicit action and records unchanged comparison prompts |
| Portability | CSV/JSON export/import, synthetic demo, local storage and documented setup | Clean clone works without API keys or a hosted account; export round-trip preserves evidence references |

## Minimal data model

- **Project:** ID, name, brand aliases, owned domains, competitors, audience, language, market.
- **PromptVersion:** stable prompt ID, version, exact text, group, buyer scenario, active state.
- **Run:** ID, frozen prompt/provider manifest, configuration hash, start/end, repetitions, budget, state.
- **Answer:** ID, run and prompt-version references, repetition, collection method, provider, requested/returned model, search backend, search enabled/invoked/unknown, locale, timestamp, status, text, raw artifact reference, final citations, retrieved sources, token/cost metadata when available.
- **Assessment:** answer ID, brand labels, evidence spans, claim checks and authoritative URLs, reviewer, scorer version, review state.
- **Action/Experiment:** linked prompts/pages, rationale, hypothesis, owner, before-state, changes, shipped date, follow-up results.

Store answer evidence immutably; review corrections are separate records. Distinguish captured, incomplete, failed and blocked. Provider-reported cost coverage must be explicit; an unknown cost is not zero.

## Metric definitions

- Discovery recommendation rate: completed eligible unbranded answers recommending the brand / completed eligible unbranded answers. Mention rate uses mentions instead. Count each brand once per answer.
- Competitor recommendation frequency uses the same denominator. Multiple brands can appear, so percentages may sum above 100%. This is not market share.
- Owned citation rate: completed answers with at least one final citation on an owned domain / completed answers in the selected cohort. Also show citation capability and coverage. Retrieved URLs do not count as final citations.
- Citation source map: count distinct answers citing each canonical URL, deduplicated within an answer. Normalize tracking parameters while retaining original evidence URLs.
- Checked-claim accuracy: verified-correct claims / adjudicated claims; show unchecked and unresolved counts. Selected checks do not represent accuracy of the entire answer set.
- Sentiment: optional reviewer-assessed positive/mixed/negative/unknown framing with evidence; separate from factual accuracy and recommendation.
- Change over time: percentage-point deltas only for matched prompt versions, routes/models, search settings and repetition design. Highlight configuration changes and incomplete coverage.

## Technical approach

The 0.1 implementation uses a TypeScript dashboard/local API, SQLite, raw JSON files and one Python CLI coordinator with configurable provider adapters. Hosted deployments can add authenticated access, a relational database and object storage through documented adapters.

Keys remain server-side or in the local runner's environment, never browser bundles, source control or exported records. Include a blank .env.example, ignored output/key paths, request timeouts, API error redaction, budget caps and safe rendering of model text. Do not execute instructions contained in collected answers.

## Research method included in the tutorial

Use buyer questions grounded in customer/support research. Separate discovery from named-brand tests. Repeat important prompts at least three times under fixed settings to expose variability; describe that as a practical pilot, not statistical proof. Preserve an unchanged cluster during content experiments. Pair visibility with page-level search performance and qualified sign-ups when available; attribution remains limited without a controlled design.

A sample pilot with 16 prompts across four configured routes produces 64 answers at one repetition. If a Gemini model runs through a third-party API, its provider and search backend stay attached to every record and the results are not pooled with direct Google grounding. Retrieved sources are not final citations. Project-specific labels are manually reviewed and never become a universal hard-coded brand scorer.

## Public 0.1 implementation and remaining work

The open-source reference is `tools/prompt-tracker` in this repository. It uses Vite/React, a loopback-only local API, Node SQLite and a Python-standard-library API runner. It contains synthetic prompts, no client answers, no private hosting authentication or deployment dependency, no private project IDs, no hard-coded company scoring, and no captured-seed merge behavior. Recommendation labels require human review. It is licensed under this repository's MIT license.

Implemented: multi-project dashboard, prompt versioning, manual/CSV capture, SQLite persistence with stale-write protection, JSON backups, evidence display, action/experiment logs, four configurable provider adapters, durable request cap, run manifests and resumability. Raw output stays alongside captures; the import CSV includes a pointer to it.

Still required for the full PRD: automated classification with evidence spans and reviewer history; model/run/configuration filters and automated matched-cohort comparisons; dollar-budget estimates; recurring scheduling; authenticated hosted adapters; analytics imports; and Automated Google AI Overviews SERP collection. The 0.1 runner does not automatically continue paused Anthropic tool turns: it preserves them as incomplete. Network fixtures verify parsing, but provider access and compatibility must be verified with the user's account. Gemini direct access depends on Google project permissions and billing; an explicitly routed alternate provider remains a separate cohort.

Release verification for 0.1: clean dependency installation, synthetic tests, dashboard build, local API/browser checks, export/import review and secret/private-binding scan. The learning guide explains how to configure model IDs and keys, why unreviewed labels are excluded, and how to separate Gemini from AI Overviews.

## Delivery milestones

A. Portable local demo and documented schema.
B. Four adapters and resumable, budgeted runs.
C. Evidence review, metrics and action reports.
D. Clean-install verification, secret scan, synthetic fixtures and public learning guide.

Release gate: a new user can run four prompts across four configured providers, inspect 16 durable results or explicit provider failures, resume without duplicate completed calls, audit each rate, and export/import the project. Critical tests cover denominator handling, citations versus retrieved sources, negative mentions, prompt history, resumability, provider failure and absence of secrets in exports.

Success: time to first useful report; fraction of results with complete provenance; fraction of recommendations linked to evidence and a next action. A higher brand visibility score is not a product success requirement.
