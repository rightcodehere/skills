---
name: rightcode-skill-updater
description: >
  Syncs the local rightcode-* skills folder with upstream sources
  (mattpocock/skills and awesome-skills/code-review-skill). Detects new
  skills or changed files not yet in this repo, presents a diff summary, and
  applies selected updates with the rightcode- prefix convention intact.
  Use when you want to check for upstream skill updates, pull in new skills
  from upstream, see what changed upstream, or run "skill updater", "sync skills",
  "update skills", "upstream diff", "check for new skills".
disable-model-invocation: true
argument-hint: "[check|sync|diff <skill-name>]"
---

# RightCode Skill Updater

Keeps this repo in sync with the upstream skill sources. Read [SOURCES.md](./SOURCES.md) for the full source-to-local mapping table before starting.

Reusable scripts live in [scripts/](./scripts/). They are plain Python 3 — no extra packages needed. Run them with `python` on Windows, macOS, or Linux.

---

## Prerequisites — GitHub Auth

**Critical:** `gh` must be authenticated to **github.com specifically** before running any command.

```powershell
# Check if already logged in to github.com
gh auth status --hostname github.com

# If not logged in (or only logged in to a GHE instance):
gh auth login --hostname github.com
```

> **GHE gotcha:** If your organisation uses GitHub Enterprise, `gh` is authenticated to your GHE host by default — **not** to github.com. The upstream skill repos are on github.com. You must always pass `--hostname github.com` on every `gh api` call, or the call will hit your GHE instance and return 404.
>
> **Rate limits:** Unauthenticated github.com calls are capped at **60 requests/hour** — enough for ~2 skills before hitting the limit. Authenticated calls get **5 000/hour**. Always authenticate before running a full sync.

---

## Commands

| Invocation | What it does |
|---|---|
| `/rightcode-skill-updater check` | Scan all upstreams; report new skills and changed files |
| `/rightcode-skill-updater sync` | Interactive: pick which updates to apply |
| `/rightcode-skill-updater diff <skill-name>` | Show line-level diff for one local skill vs its upstream |

If the user runs the skill with no argument, run **check** first, then offer to continue with **sync**.

---

## Execution — Use the Scripts

The scripts handle all phases automatically. They require **Python 3.8+** and the `gh` CLI — no pip installs.

- **macOS / Linux**: Python 3 is pre-installed. `python3 check.py` or `python check.py`.
- **Windows**: Download from https://python.org if needed. Use `python check.py` in any terminal.

### check (Phase 1 + 2)

```bash
# From any directory — works on Windows, macOS, Linux
python skills/rightcode-skill-updater/scripts/check.py
```

The script:
- Verifies `gh auth --hostname github.com` before doing anything.
- Scans `engineering`, `productivity`, `misc`, and `in-progress` for new upstream skills.
- Diffs every mapped skill file against its local copy.
- Checks `awesome-skills/code-review-skill` reference files.
- Saves a `report.json` to a temp directory and prints the path.
- Prints the summary and, if there are changes, shows the `apply.ps1` command to run next.

### sync (Phase 3 + 4)

```bash
# Pass the report path printed by check.py
python skills/rightcode-skill-updater/scripts/apply.py --report-path "<path from check output>"
```

The script walks through each changed/new skill, asks `[y/n/file-by-file]`, and writes only the approved files.

---

## What the Scripts Do (Phase Reference)

### Phase 1 — Detect new upstream skills

Scans `engineering`, `productivity`, `misc`, and `in-progress` categories in `mattpocock/skills`. Any folder not in the SOURCES.md mapping table (and not in the skip list) is flagged as **NEW**.

All `gh api` calls use `--hostname github.com`. Base64 content is decoded with Python's `base64.b64decode()` — works identically on every OS.

### Phase 2 — Diff mapped skills

For each mapped skill, every tracked file is fetched and compared to its local copy using `Compare-Object` on normalised lines (CRLF → LF before comparing). Changed files are stored in the report with `+add / -del` counts and the upstream content cached for apply.

### Phase 3 — Interactive confirmation

`apply.ps1` asks per skill: `[y / n / file-by-file]`. Nothing is written until confirmed.

### Phase 4 — Write approved files

- `write_skill_file()` uses `pathlib.Path` — handles separators correctly on every OS.
- For new skills, `name:` in `SKILL.md` frontmatter is rewritten to `rightcode-<name>` via regex.
- After adding a new skill, a reminder is printed to update [SOURCES.md](./SOURCES.md).

---

## Manual API Reference

If you need to run one-off queries (e.g. for `diff <skill-name>`):

```bash
# Always include --hostname github.com

# List skills in a category
gh api --hostname github.com repos/mattpocock/skills/contents/skills/engineering --jq '[.[] | select(.type=="dir") | .name]'

# List files in a skill folder
gh api --hostname github.com repos/mattpocock/skills/contents/skills/engineering/tdd --jq '[.[].name]'

# Fetch and decode a file (Python one-liner — works on Windows, macOS, Linux)
gh api --hostname github.com repos/mattpocock/skills/contents/skills/engineering/tdd/SKILL.md --jq '.content' | python -c "import sys,base64,re; print(base64.b64decode(re.sub(r'\\s','',sys.stdin.read())).decode())"

# awesome-skills/code-review-skill — SKILL.md is at repo root (not in a skills/ subfolder)
gh api --hostname github.com repos/awesome-skills/code-review-skill/contents/SKILL.md --jq '.content'
```

---

## Adding a new skill (manual fallback)

If the interactive script is not available:

1. Create `skills/rightcode-<name>/`.
2. Download each file via the API (decode base64 with PowerShell as shown above).
3. Set `name: rightcode-<name>` in `SKILL.md` frontmatter.
4. **For mattpocock/skills**: update any bare skill invocation references (`diagnose` → `rightcode-diagnose`).
5. **For awesome-skills/code-review-skill**: mirror reference files into the local `reference/` subfolder.
6. Add the mapping row to [SOURCES.md](./SOURCES.md).

---

## Phase 5 — Post-sync Checklist

After writing all changes:

- [ ] Run `get_errors` (or equivalent lint) on changed SKILL.md files to catch YAML frontmatter issues.
- [ ] Show the user a summary of what was written.
- [ ] Remind the user to test the updated skills before publishing.
- [ ] Do **not** commit, push, or publish automatically — wait for explicit user confirmation per working-style preferences.

---

## Handling Edge Cases

| Situation | Action |
|---|---|
| `gh` authenticated to GHE, not github.com | Run `gh auth login --hostname github.com`; always pass `--hostname github.com` on every API call |
| `gh` not authenticated at all | Run `gh auth login --hostname github.com` |
| Rate limit hit (HTTP 403, 60/hr) | Authenticate to github.com — authenticated limit is 5 000/hr |
| `base64 -d` not available (Windows) | Use `[System.Convert]::FromBase64String()` — the scripts already do this |
| Upstream repo returns 404 | Verify repo still exists; update SOURCES.md if renamed/moved |
| Upstream file is binary or non-text | Skip with a warning |
| Local skill has diverged intentionally (custom edits) | Show the diff and let the user decide — never auto-overwrite |
| New upstream sub-folder inside an existing skill (e.g. `scripts/new.py`) | Treat as a new file; `check.ps1` will surface it |
| Upstream adds a skill already covered by a local-only skill | Flag as a potential conflict; do not auto-merge |
| Python not installed on Windows | Download from https://python.org (3.8+) |
