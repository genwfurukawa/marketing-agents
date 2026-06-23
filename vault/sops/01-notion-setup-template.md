---
type: sop
status: active
owner: {{OWNER}}
created: {{date}}
updated: {{date}}
tags: [sop, notion, onboarding]
---

# SOP: Notion Setup (Workspace + Per-Client Hub)

> Stand up the Notion integration, configure the repo to use it, and scaffold a per-client Marketing Hub with databases and strategy pages.

## Trigger

Run this SOP when any of these happen:

- First-time setup of the `{{REPO_NAME}}` ops repo on a new machine or for a new operator.
- Onboarding a new client who needs their own Marketing Hub in Notion.
- The Notion integration token has been rotated or revoked and needs to be re-issued.

## Inputs

Required before you start:

- Admin access to the Notion workspace where the HQ page will live.
- Access to the `{{REPO_NAME}}` repo (clone with push rights).
- Python 3.10+ installed locally.
- `pip` available for installing dependencies.
- The `.env` file at the repo root (create it if missing — it is gitignored).

Prior SOPs: none. This is the foundation.

## Steps

### Part A — One-time workspace setup

Run Part A once per workspace. Skip to Part B if the integration and HQ page already exist.

1. **Create the Notion integration.**
   - Go to https://www.notion.so/profile/integrations
   - Click `New integration`
   - Name: `{{INTEGRATION_NAME}}`
   - Associated workspace: the workspace that will host the HQ page
   - Type: `Internal`
   - Capabilities: Read content, Update content, Insert content. Leave user capabilities at `No user information`.
   - Click `Save`
   - Expected result: integration page shows an `Internal Integration Secret` starting with `ntn_` or `secret_`.

2. **Copy the integration token.**
   - On the integration page, click `Show` next to the secret, then copy it.
   - Expected result: token copied to clipboard. Treat it like a password.

3. **Store the token in `.env`.**
   - Open (or create) `{{REPO_ROOT_PATH}}/.env`
   - Add the line:
     ```
     NOTION_TOKEN=ntn_your_token_here
     ```
   - Save the file.
   - Expected result: `grep NOTION_TOKEN .env` returns the line.

4. **Verify `.env` is gitignored.**
   - Check the repo root `.gitignore` contains a line matching `.env`.
   - Run:
     ```bash
     git check-ignore -v .env
     ```
   - Expected result: output shows `.gitignore:<line>:.env   .env`. If not, add `.env` to `.gitignore` before touching the token. Never commit `.env`.

5. **Install Python dependencies.**
   ```bash
   pip install notion-client python-dotenv
   ```
   Expected result: both packages install without errors.

6. **Create the HQ page in Notion.**
   - In Notion, at the top level of your workspace (or wherever you want the root), create a new page titled `{{HQ_PAGE_NAME}}`.
   - Leave the body empty for now. This page is the parent for all client Marketing Hubs.
   - Expected result: the page exists and you can navigate to it.

7. **Grant the integration access to the HQ page.**
   - Open the `{{HQ_PAGE_NAME}}` page.
   - Click the `...` menu in the top right, then `Connections` -> `Connect to` -> search for `{{INTEGRATION_NAME}}` -> `Confirm`.
   - Expected result: the integration appears in the page's connections list. Access propagates to all children of this page automatically.

8. **Capture the HQ page ID.**
   - In Notion, click `Share` on the HQ page and `Copy link`, or use `...` -> `Copy link`.
   - The URL looks like: `https://www.notion.so/{{HQ_PAGE_NAME_KEBAB}}-{{HQ_PAGE_ID_UNHYPHENATED}}`
   - The final 32-char hex string is the page ID. Hyphenate it into UUID form.
   - Add to `.env`:
     ```
     NOTION_HQ_PAGE_ID={{HQ_PAGE_ID}}
     ```
   - Expected result: `.env` now contains both `NOTION_TOKEN` and `NOTION_HQ_PAGE_ID`.

### Part B — Per-client hub setup

Run Part B every time you onboard a new client.

9. **Confirm prerequisites.**
   - `.env` has `NOTION_TOKEN` and `NOTION_HQ_PAGE_ID` set.
   - Dependencies installed (Part A step 5).
   - Integration is connected to the HQ page (Part A step 7).

10. **Run the scaffolding script.**
    ```bash
    python scripts/notion_setup_client.py "{{EXAMPLE_CLIENT_NAME}}"
    ```
    Replace `"{{EXAMPLE_CLIENT_NAME}}"` with the real client name in quotes.

    Expected result: terminal prints step-by-step progress:
    ```
    Setting up Notion workspace for: {{EXAMPLE_CLIENT_NAME}}
    Parent HQ page: <hq id>
      -> Creating hub page: {{EXAMPLE_CLIENT_NAME}} - Marketing Hub
      -> Creating Content Calendar database
      -> Creating Deliverables database
      -> Creating Reports page
      -> Creating Strategy page
         -> Creating sub-page: Positioning & ICP
         -> Creating sub-page: Brand Voice
         -> Creating sub-page: Competitive Landscape
      -> Linking children in hub page body
    Done. All resources created successfully.
    ```

11. **Capture the printed env block.**
    The script prints a block at the end that looks like:
    ```
    # --- Notion IDs for {{EXAMPLE_CLIENT_NAME}} ---
    NOTION_CLIENT_SLUG={{example_client_slug}}
    NOTION_CLIENT_HUB_PAGE_ID=...
    NOTION_CONTENT_CALENDAR_DB_ID=...
    NOTION_DELIVERABLES_DB_ID=...
    NOTION_REPORTS_PAGE_ID=...
    NOTION_STRATEGY_PAGE_ID=...
    NOTION_STRATEGY_POSITIONING_ICP_PAGE_ID=...
    NOTION_STRATEGY_BRAND_VOICE_PAGE_ID=...
    NOTION_STRATEGY_COMPETITIVE_PAGE_ID=...
    # ----------------------------------
    ```

12. **Store the client IDs.**
    - Append the entire block to the client's own `.env` (when they get their own cloned ops repo via [[clone-ops]]-style setup), OR
    - If operating from this shared repo, append to `.env` under a clearly labeled section so multiple clients can coexist.
    - Expected result: the IDs are persisted somewhere Claude Code and the Notion MCP can read them.

13. **Verify in Notion.**
    - Open the HQ page in Notion.
    - Confirm a child page titled `{{EXAMPLE_CLIENT_NAME}} - Marketing Hub` with a rocket emoji exists.
    - Click in. Confirm you see the Content Calendar and Deliverables databases, plus Reports and Strategy pages, and that Strategy has three sub-pages.

## Checks

- [ ] `NOTION_TOKEN` present in `.env`
- [ ] `NOTION_HQ_PAGE_ID` present in `.env`
- [ ] `.env` is ignored by git (`git check-ignore .env` returns a match)
- [ ] Integration `{{INTEGRATION_NAME}}` is connected to the HQ page
- [ ] `{{HQ_PAGE_NAME}}` page exists in Notion
- [ ] For each client: `[Client Name] - Marketing Hub` page exists under HQ
- [ ] Client hub contains two databases (Content Calendar, Deliverables) and two pages (Reports, Strategy)
- [ ] Strategy page contains three sub-pages (Positioning & ICP, Brand Voice, Competitive Landscape)
- [ ] Client-specific env block is stored somewhere the system can read it

## Outputs

After this SOP runs:

- A Notion integration named `{{INTEGRATION_NAME}}` with its token in `.env`.
- A `{{HQ_PAGE_NAME}}` page in Notion with the integration connected.
- One or more `{Client Name} - Marketing Hub` pages, each with:
  - Content Calendar database (Title, Type, Status, Publish Date, Notes)
  - Deliverables database (Name, Type, Status, Due Date, Link)
  - Reports page
  - Strategy page with sub-pages: Positioning & ICP, Brand Voice, Competitive Landscape
- Env vars captured: `NOTION_CLIENT_SLUG`, `NOTION_CLIENT_HUB_PAGE_ID`, `NOTION_CONTENT_CALENDAR_DB_ID`, `NOTION_DELIVERABLES_DB_ID`, `NOTION_REPORTS_PAGE_ID`, `NOTION_STRATEGY_PAGE_ID`, `NOTION_STRATEGY_POSITIONING_ICP_PAGE_ID`, `NOTION_STRATEGY_BRAND_VOICE_PAGE_ID`, `NOTION_STRATEGY_COMPETITIVE_PAGE_ID`.

## Escalation

- **Symptom:** Script exits with `NOTION_TOKEN not set in .env`.
  **Fix:** `.env` is missing or not at the repo root. Confirm the file exists at `{{REPO_ROOT_PATH}}/.env` and contains `NOTION_TOKEN=...` with no quotes and no trailing spaces.

- **Symptom:** `APIResponseError: Could not find page with ID` or `object_not_found`.
  **Fix:** The integration is not connected to the HQ page. Repeat Part A step 7. Remember: integration access propagates to children, so connecting at HQ is enough for everything underneath.

- **Symptom:** `unauthorized` (401).
  **Fix:** Token is wrong, expired, or revoked. Re-run Part A steps 1-3 to issue a new token. Rotate in `.env`.

- **Symptom:** `validation_error` on database creation.
  **Fix:** Usually a property schema mismatch. Check that the Notion API version supported by `notion-client` matches what the script is sending. Upgrade: `pip install -U notion-client`.

- **Symptom:** Script fails partway through. Terminal shows `Partial progress` with a list of IDs already created.
  **Fix:** Go to Notion, find the orphan resources by the printed IDs, and delete them. Then re-run the script with the same client name. The script is not idempotent — it will happily create duplicates if you skip cleanup.

- **Symptom:** HQ page ID is rejected as invalid.
  **Fix:** Notion page IDs are 32 hex chars. The script accepts both hyphenated UUID form and unhyphenated. Make sure you grabbed the ID from the URL, not the share link hash.

- **Who to ping:** {{OWNER}} for strategic calls on structure. For execution failures, re-run with Claude Code and paste the error.

## Notes

- The script creates everything under `NOTION_HQ_PAGE_ID`. If you want client hubs in a different parent, change that env var temporarily before running.
- Databases are `is_inline: False` (standalone pages), not inline blocks. The hub page body uses `link_to_page` blocks to surface them with icons.
- Emoji icons are hardcoded in the script: 🚀 hub, 📅 content calendar, 📦 deliverables, 📊 reports, 🧭 strategy, 🎯 positioning, 🗣️ brand voice, ⚔️ competitive.
- The slug logic lowercases, replaces spaces with underscores, `&` with `and`, and `/` with `-`.
- Related: [[00-index]], [[sop-template]]
- Source of truth: `scripts/notion_setup_client.py`

---

## Placeholders

When instantiating this template for a specific repo, replace:

- `{{REPO_NAME}}` — name of the ops/agency repo (e.g., "Acme Ops")
- `{{REPO_ROOT_PATH}}` — absolute path to the repo root on the operator's machine
- `{{INTEGRATION_NAME}}` — name of the Notion integration (typically matches `{{REPO_NAME}}`)
- `{{HQ_PAGE_NAME}}` — name of the parent Notion page (e.g., "Acme HQ")
- `{{HQ_PAGE_NAME_KEBAB}}` — kebab-case form for URL (e.g., "Acme-HQ")
- `{{HQ_PAGE_ID}}` — UUID of the HQ page in Notion
- `{{HQ_PAGE_ID_UNHYPHENATED}}` — same ID without hyphens (URL form)
- `{{EXAMPLE_CLIENT_NAME}}` — sample client name used in code examples (e.g., "Acme Robotics")
- `{{example_client_slug}}` — slug form of the example client
- `{{OWNER}}` — owner of this SOP (typically the founder or operator)
- `{{date}}` — today's date in YYYY-MM-DD form
