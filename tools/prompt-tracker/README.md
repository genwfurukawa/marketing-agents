# SuperMarketers Prompt Tracker

An MIT-licensed, local-first dashboard for buyer-question research across OpenAI, Gemini, Claude and Perplexity APIs. Save answers, inspect citations, review recommendations, and connect findings to content changes. No private hosting account, ChatGPT sign-in, client dataset or company-specific scoring is required.

**Release 0.1 is a learning tool:** manual/CSV capture, local SQLite persistence, four provider adapters and resumable CLI runs. Recommendation scoring is human-reviewed. Schedules, analytics integrations, automated classification and Google AI Overviews API collection remain roadmap items. Actual model availability and search-tool support depend on your provider account.

## Start the dashboard

Requirements: Node 22.13+ (Node 24 recommended), npm, Python 3.10+ for API collection.

```bash
git clone https://github.com/genwfurukawa/marketing-agents.git
cd marketing-agents/tools/prompt-tracker
npm ci
npm run dev
```

Open the localhost URL printed by Vite. The synthetic Demo Studio project contains four example prompts and no real results. Create your project, add buyer questions and competitors, then export a JSON backup. Data saves to `.data/workspace.sqlite` on this computer. No account setup is needed. Local operation is not a hosted multi-user service; keep the default loopback binding. `npm run build` and `npm start` serve the built dashboard locally with the same SQLite API.

## Run your own API cohort

1. Copy `.env.example` to `.env` and supply your own API keys. Never commit that file.
2. Copy `examples/providers.json` to an ignored local location such as `.data/providers.json`. Replace every model placeholder with an exact available model ID. Select only models supporting the enabled web-search tool. Removing a route is an explicit partial cohort.
3. Save the dashboard's JSON backup as `.data/workspace.json`; use your project ID from that file. For a no-network setup check, use `examples/workspace.json` and project `demo` after replacing the model placeholders.

```bash
python3 scripts/run.py --workspace .data/workspace.json --config .data/providers.json --project YOUR_PROJECT_ID --output captures/round-1 --env .env --dry-run
python3 scripts/run.py --workspace .data/workspace.json --config .data/providers.json --project YOUR_PROJECT_ID --output captures/round-1 --env .env
node scripts/import-captures.mjs .data/workspace.json captures/round-1 .data/answers.csv
```

Import the CSV in **Answer evidence**. Read each result, select **Edit capture**, correct brand recommendation labels, and confirm the review checkbox. Until reviewed, results contribute to captured-answer/citation counts but not recommendation rates. A mention, a conditional recommendation, and an overall comparison winner are different observations. Use notes to retain the exact supporting passage and conditions.

Four prompts × four providers × one repetition = 16 results. Sixteen prompts gives 64. The example cap allows 20 HTTP requests, including retries; it is not a dollar budget. Search-tool calls can have their own costs. Review provider pricing and token limits before execution. The cap is durable across resume; increase it explicitly when necessary. Successful records are skipped; failed/incomplete attempts are archived. Changed prompts, models, search settings or repetitions require a new output folder. Use a new folder for every new round, even with identical configuration.

No new paid API calls are required to open the dashboard or run tests. An interrupted process after a provider accepts a request may incur a charge without a saved result; exactly-once billing cannot be guaranteed.

## What each surface means

| Label | Default collection route | What it measures |
|---|---|---|
| ChatGPT | OpenAI Responses API + web search | The configured OpenAI API model, not the ChatGPT consumer app |
| Gemini | Google Gemini Interactions API + Google Search grounding | The configured Gemini model and its search tools, not Google AI Overviews |
| Claude | Anthropic Messages API + web search | The configured Claude API model, not claude.ai |
| Perplexity | Perplexity Agent API + explicit model and web search | This Perplexity API route; the returned model may be another vendor's model |

An optional Gemini route through Perplexity is explicit: set `label` to `Gemini`, `provider` to `Perplexity`, `model` to an available `google/...` model, and `searchBackend` to `Perplexity web search`. There is no automatic fallback. Keep this cohort separate from direct Google grounding.

Google AI Overviews is a Google Search result feature, separate from Gemini. This release supports manual capture using the `Google AI Overviews` surface. Retain exact query, location, language, device, time, full Overview and references. A successful search with no Overview is an absence observation; failed access is missing evidence. Do not convert a Gemini answer into an Overview. Automated collection is a future SERP adapter. DataForSEO documents an `ai_overview` result type and an optional `load_async_ai_overview` field; validate availability, terms, and current per-call charges before using it. Keep any cost-controlled SERP run separate from model API runs.

Official references: [OpenAI web search](https://developers.openai.com/api/docs/guides/tools-web-search), [Anthropic web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool), [Gemini grounding](https://ai.google.dev/gemini-api/docs/google-search), [Perplexity Agent API](https://docs.perplexity.ai/docs/agent-api/models), [DataForSEO Google SERP fields](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/).

## Evidence and interpretation

Keep original JSON under the run folder; CSV is the dashboard import format, not a replacement for raw artifacts. Only final citations count toward citation metrics; fetched pages without citation support are retrieved sources. Manually verified claims are a selected subset, not whole-batch accuracy. Multiple competitor recommendations can occur in one answer, so frequencies can sum above 100%.

The dashboard currently filters by date, surface and collection method. Model/run-specific filtering and an automated matched-cohort comparison are roadmap work: inspect provenance or create separate projects before making before/after claims. Aggregated time trends do not establish causal lift. Export CSV/JSON for cohort analysis; connect sign-up data separately.

## Validation and contributing

```bash
npm test
npm run build
npm audit
```

Tests cover reviewed denominators, citations vs retrieval, CSV safety, SQLite persistence/concurrency, immutable run identity, explicit routing and incomplete output. Network adapters have fixture tests; account-specific live access is not guaranteed. Direct Gemini requires an enabled Google API project and may be unavailable due to account permissions or billing. If you explicitly route Gemini through another provider, record that provider and search backend; keep it separate from direct Google-grounded results. Unsupported provider response states are preserved as incomplete rather than scored.

Read the [PRD](../../docs/prds/prompt-tracker.md). Contributions should include synthetic provider-response fixtures and preserve provenance. Never submit keys, customer prompts, raw client captures or local databases. Use the repository's MIT license; dependencies retain their own licenses.
