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

---

## Commands

| Invocation | What it does |
|---|---|
| `/rightcode-skill-updater check` | Scan all upstreams; report new skills and changed files |
| `/rightcode-skill-updater sync` | Interactive: pick which updates to apply |
| `/rightcode-skill-updater diff <skill-name>` | Show line-level diff for one local skill vs its upstream |

If the user runs the skill with no argument, run **check** first, then offer to continue with **sync**.

---

## Phase 1 — Fetch Upstream State

Use the GitHub Contents API via the `gh` CLI. Never `git clone` — use API calls only (read-only, no local side effects).

**mattpocock/skills** — skills are nested under category subfolders, not flat:
```powershell
# Skills live at skills/<category>/<name>/ — scan each tracked category
gh api repos/mattpocock/skills/contents/skills/engineering --jq '[.[] | select(.type=="dir") | .name]'
gh api repos/mattpocock/skills/contents/skills/productivity --jq '[.[] | select(.type=="dir") | .name]'
gh api repos/mattpocock/skills/contents/skills/misc --jq '[.[] | select(.type=="dir") | .name]'

# List files inside a specific skill folder
gh api repos/mattpocock/skills/contents/skills/engineering/tdd --jq '.[].name'

# Fetch a specific file
gh api repos/mattpocock/skills/contents/skills/engineering/tdd/SKILL.md --jq '.content' | base64 -d
```

**awesome-skills/code-review-skill** — single-skill repo, `SKILL.md` is at the repository root:
```powershell
# SKILL.md is at root, not inside a skills/ folder
gh api repos/awesome-skills/code-review-skill/contents/SKILL.md --jq '.content' | base64 -d

# List reference files
gh api repos/awesome-skills/code-review-skill/contents/reference --jq '[.[].name]'

# Fetch a reference file
gh api repos/awesome-skills/code-review-skill/contents/reference/typescript.md --jq '.content' | base64 -d
```

> If `gh` is not available, fall back to `Invoke-RestMethod` against `https://api.github.com/repos/{owner}/{repo}/contents/...`. No auth required for public repos.

---

## Phase 2 — Build the Change Report

Cross-reference the upstream folders with the mapping table in [SOURCES.md](./SOURCES.md).

### 2a — New skills (upstream has, local does not)

For each upstream skill folder that has **no matching local folder** in the mapping table:
- Mark as **NEW — not yet in this repo**.
- Fetch its full file list so you can show what would be added.
- Note its upstream category path (e.g. `skills/engineering/new-thing`).

### 2b — Changed files (upstream differs from local)

For each mapped skill, compare every file that exists in both:
1. Fetch the upstream file content.
2. Read the local file content.
3. Produce a unified diff (use PowerShell `Compare-Object` on lines, or write the two versions to temp files and run `git diff --no-index`).
4. If there are differences, mark the skill as **CHANGED** and record the differing files.

### 2c — Local-only skills

Skills listed under "Local-only Skills" in SOURCES.md are skipped — they have no upstream to diff against. This includes all `rightcode-codeprobe-*` sub-skills.

### 2d — Produce the summary

Print a report in this format:

```
## Upstream Sync Report  (<date>)

### New Skills (N)
- upstream: <folder>  →  would become: rightcode-<folder>
  Files: SKILL.md, scripts/foo.py, ...

### Changed Skills (N)
- rightcode-<name>
  Changed files: SKILL.md (+12 / -3), scripts/bar.js (+5 / -0)

### Unchanged Skills (N)
- rightcode-<name>, ...

### Local-only Skills (not checked)
- rightcode-code-review, rightcode-migrate-to-shoehorn, ...
```

Ask the user: "Would you like to review and apply any of these changes? (yes / select / no)"

---

## Phase 3 — Interactive Sync (sync command only)

If the user says **yes** or **select**:

1. For each **NEW** skill, ask: "Add `rightcode-<name>`? [y/n]"
2. For each **CHANGED** skill, show the per-file diffs and ask: "Apply changes to `rightcode-<name>`? [y/n/file-by-file]"
   - If "file-by-file", ask for each differing file individually.
3. Once selections are confirmed, proceed to Phase 4.

Do **not** apply anything without explicit per-skill confirmation.

---

## Phase 4 — Apply Changes

### Adding a new skill

1. Create the folder `skills/rightcode-<name>/`.
2. Copy each upstream file, downloading via the GitHub API.
3. In `SKILL.md` frontmatter, set `name:` to `rightcode-<name>` to follow local convention.
4. **For mattpocock/skills**: update any internal cross-skill references that used bare upstream names (e.g. skill invocations referencing `diagnose` should become `rightcode-diagnose`).
5. **For awesome-skills/code-review-skill**: if adding reference files, mirror them into the local skill's `reference/` subfolder.
6. Add the new mapping row to [SOURCES.md](./SOURCES.md).

### Updating an existing skill

1. For each approved file, write the upstream content to the local path.
2. Do **not** overwrite local files that were not in the approved list.

### Naming convention rules

- Folder name: always `rightcode-<upstream-name>` (no double prefix).
- SKILL.md frontmatter `name:` field must match the folder name exactly.
- All internal `[link](./path)` references are relative and need no changes.

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
| `gh` CLI not authenticated | Tell the user to run `gh auth login` and retry |
| Upstream repo renamed or moved | Update SOURCES.md and notify the user |
| Upstream file is binary or non-text | Skip with a warning |
| Local skill has diverged intentionally (custom edits) | Show the diff and let the user decide — never auto-overwrite |
| New upstream sub-folder inside an existing skill (e.g. `scripts/new.py`) | Treat as a **CHANGED** file and include in diff |
| Upstream adds a skill already covered by a local-only skill | Flag as a potential conflict; do not auto-merge |
