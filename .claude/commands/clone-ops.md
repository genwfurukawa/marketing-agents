---
description: Scaffold a new standalone client repo at ~/clients/{slug}/ from the canonical template. Creates the 9-folder structure, stub configs, optional git init + GitHub repo, and a combined VS Code workspace.
argument-hint: <slug> [--name "Full Client Name"] [--no-git] [--no-workspace] [--no-github]
---

You are scaffolding a new client repo from the canonical template.

## Arguments

Parse from `$ARGUMENTS`:
- `slug` (positional, required): lowercase, hyphens for spaces, no special chars. Example: `acme-corp`.
- `--name "Full Name"` (optional): display name for README/docs. Defaults to title-cased `slug`.
- `--no-git`: skip `git init` and initial commit.
- `--no-github`: skip the GitHub repo creation prompt (implies local-only).
- `--no-workspace`: skip creating `{slug}.code-workspace`.

If `slug` is missing or invalid (not lowercase/hyphenated), STOP and tell the user.

## Step 1: Resolve Paths and Pre-flight

- `methodology_root` = current working directory (must be the methodology repo — check that `.claude/commands/clone-ops.md` exists relative to it)
- `client_root` = `~/clients/{slug}/` (expand `~` to `$HOME`)
- `templates_root` = `{methodology_root}/templates/client-scaffold`

Verify:
1. `{client_root}` does NOT exist. If it does, STOP and ask the user.
2. `{templates_root}/README.md.tmpl` exists. If not, STOP — prerequisite templates missing.
3. `{methodology_root}/templates/brand_brain/BRAND_BRAIN_TEMPLATE.md` exists.

## Step 2: Create the Canonical Folder Structure

```bash
mkdir -p {client_root}/{config,brand,research,vault,production,playbooks,ops}
mkdir -p {client_root}/intelligence/{scans,scorecards,gaps}
mkdir -p {client_root}/intelligence/strategy/reflections
mkdir -p {client_root}/content/{linkedin,email,blog}
# Engine: Brain, Gates, Ledger, and the drafts-in-flight folder (ENGINE_PRD.md 7.2)
mkdir -p {client_root}/brain/proof
mkdir -p {client_root}/gates
mkdir -p {client_root}/ledger/reports
mkdir -p {client_root}/production/drafts
```

Drop `.gitkeep` files into every empty leaf folder so they survive git:
- `brand/.gitkeep`
- `research/.gitkeep`
- `vault/.gitkeep`
- `production/.gitkeep`
- `playbooks/.gitkeep`
- `ops/.gitkeep`
- `intelligence/scans/.gitkeep`, `intelligence/scorecards/.gitkeep`, `intelligence/gaps/.gitkeep`
- `intelligence/strategy/.gitkeep`
- `content/linkedin/.gitkeep`, `content/email/.gitkeep`, `content/blog/.gitkeep`
- `brain/proof/.gitkeep`, `gates/.gitkeep`, `ledger/reports/.gitkeep`, `production/drafts/.gitkeep`

## Step 3: Render Root Files from Templates

For each `*.tmpl` in `{templates_root}` (top-level only, not `config/`):
1. Read the template
2. Replace `{{slug}}` and `{{name}}` (and `{{name_title}}` = title-cased name if encountered)
3. Write to `{client_root}/` with `.tmpl` stripped

Files written at root:
- `README.md`
- `CLAUDE.md`
- `config.yaml`
- `lessons.md`
- `.gitignore` (copied verbatim from `.gitignore.tmpl` — uses `*.code-workspace` glob, no placeholders needed)

## Step 4: Render Config Stubs

For each `*.tmpl` in `{templates_root}/config/`:
1. Render with same placeholder replacement
2. Write to `{client_root}/config/` with `.tmpl` stripped

Plus: copy `{methodology_root}/templates/brand_brain/BRAND_BRAIN_TEMPLATE.md` to `{client_root}/config/brand-brain.md` (no placeholder replacement — it's a generic 12-section template).

## Step 5: Git Init (unless `--no-git`)

```bash
cd {client_root}
git init -b main
git add -A
git commit -m "feat: scaffold {slug} client repo from canonical template"
```

## Step 6: GitHub Repo (unless `--no-git` or `--no-github`)

Ask the user: "Push to GitHub as private repo `{slug}-ops`? (y/N)"

If yes:
```bash
cd {client_root}
gh repo create {slug}-ops --private --source=. --remote=origin --push
```

## Step 7: Workspace File (unless `--no-workspace`)

Write `{client_root}/{slug}.code-workspace`. The file lives inside the client repo for discoverability but is **gitignored** (Step 4's `.gitignore` uses the `*.code-workspace` glob) because its paths are machine-specific.

Use **relative** paths so the workspace survives a home-dir move. From `~/clients/{slug}/`, `../../marketing-agents` resolves to `$MARKETING_AGENTS`.

```json
{
  "folders": [
    { "name": "{name} (client)", "path": "." },
    { "name": "Methodology (SOPs)", "path": "../../marketing-agents" }
  ],
  "settings": {}
}
```

This assumes the canonical layout: client repos in `~/clients/{slug}/`, methodology at `$MARKETING_AGENTS/`. If a client sits elsewhere, adjust the relative hops.

## Step 8: Report

Output a summary:
- Client slug + display name
- Local path: `~/clients/{slug}/`
- GitHub URL (if pushed) or "local-only"
- Workspace file path (if created)
- Folder count, file count
- **Next steps:**
  1. Open `~/clients/{slug}/{slug}.code-workspace` in VS Code
  2. Fill `config.yaml` at the client repo root
  3. Run `/build-brand-brain` to populate `config/brand-brain.md`
  4. Fill remaining config files
  5. Add brand assets to `brand/`
  6. If you skipped GitHub setup, add it later with:
     `gh repo create {slug}-ops --private --source=. --remote=origin --push`

## Important Rules

- NEVER write inside `{methodology_root}` during scaffold.
- NEVER commit if a `.env` file was somehow created.
- ALWAYS verify `{client_root}` is empty/nonexistent before scaffolding.
- ALWAYS use the templates from `templates/client-scaffold/` — do not embed content inline.
