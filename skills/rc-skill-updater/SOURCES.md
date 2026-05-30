# Upstream Sources

> **Verified against live repos on 2026-05-13.** Re-verify after major upstream changes.

Two upstream sources. The codeprobe sub-skills (`rc-codeprobe-*`) are **local-only** — they were inspired by the NishilBhave blog post (https://dev.to/nishilbhave/...) but have no public upstream repo to sync against.

---

## Source 1 — mattpocock/skills

**URL**: https://github.com/mattpocock/skills  
**Structure**: `skills/<category>/<skill-name>/SKILL.md` — skills are nested under category subfolders, **not** at a flat `skills/<name>/` level.

### Categories and skills

| Category | Upstream Skill Folder | Local Folder | Notes |
|---|---|---|---|
| `engineering` | `diagnose` | `rc-diagnose` | |
| `engineering` | `grill-with-docs` | `rc-grill-with-docs` | |
| `engineering` | `improve-codebase-architecture` | `rc-improve-codebase-architecture` | |
| `engineering` | `prototype` | `rc-prototype` | |
| `engineering` | `setup-matt-pocock-skills` | `rc-setup-skills` | Upstream name differs — we renamed |
| `engineering` | `tdd` | `rc-tdd` | |
| `engineering` | `to-issues` | `rc-to-issues` | |
| `engineering` | `to-prd` | `rc-to-prd` | |
| `engineering` | `triage` | `rc-triage` | |
| `engineering` | `zoom-out` | `rc-zoom-out` | |
| `productivity` | `caveman` | `rc-caveman` | |
| `productivity` | `grill-me` | `rc-grill-me` | |
| `productivity` | `handoff` | `rc-handoff` | |
| `productivity` | `write-a-skill` | `rc-write-a-skill` | |
| `misc` | `git-guardrails-claude-code` | `rc-git-guardrails` | Upstream name differs — we shortened |
| `misc` | `migrate-to-shoehorn` | `rc-migrate-to-shoehorn` | |
| `misc` | `scaffold-exercises` | `rc-scaffold-exercises` | |
| `misc` | `setup-pre-commit` | `rc-setup-pre-commit` | |

### Upstream folders NOT tracked (skip these)

| Category | Skill | Reason |
|---|---|---|
| `personal` | `edit-article` | Personal/content skill, not engineering |
| `personal` | `obsidian-vault` | Personal/content skill, not engineering |
| `in-progress` | `review` | Upstream draft — not stable |
| `in-progress` | `writing-beats` | Personal content, out of scope |
| `in-progress` | `writing-fragments` | Personal content, out of scope |
| `in-progress` | `writing-shape` | Personal content, out of scope |
| `deprecated` | *(all)* | Deprecated by upstream |

### Upstream files NOT synced (script policy exclusions)

Upstream `.sh` scripts are excluded — this repo requires all skill scripts to be **Python only** (cross-platform). The `scripts/` subfolders for the skills below contain shell scripts that will never be synced.

| Local Folder | Excluded Upstream File | Reason |
|---|---|---|
| `rc-git-guardrails` | `scripts/block-dangerous-git.sh` | Shell script — Python-only policy; not needed (skill instructions cover the setup) |
| `rc-diagnose` | `scripts/hitl-loop.template.sh` | Shell script — Python-only policy |

### API endpoints for mattpocock/skills

```powershell
# List skills per category
gh api repos/mattpocock/skills/contents/skills/engineering --jq '.[].name'
gh api repos/mattpocock/skills/contents/skills/productivity --jq '.[].name'
gh api repos/mattpocock/skills/contents/skills/misc --jq '.[].name'

# Fetch a specific file
gh api repos/mattpocock/skills/contents/skills/engineering/tdd/SKILL.md --jq '.content' | base64 -d
```

### New upstream skill detection

When scanning, also check `in-progress` — skills may graduate from there to `engineering`/`productivity`/`misc` without notice.

---

## Source 2 — awesome-skills/code-review-skill

**URL**: https://github.com/awesome-skills/code-review-skill  
**Structure**: **Single-skill repo** — `SKILL.md` lives at the repository root (not inside a `skills/` subfolder). Supporting files sit alongside it.

```
awesome-skills/code-review-skill/
├── SKILL.md              ← root-level, tracks as: rc-code-review
├── reference/            ← language/framework reference guides
│   ├── angular.md
│   ├── architecture-review-guide.md
│   ├── code-quality-universal.md
│   ├── code-review-best-practices.md
│   ├── common-bugs-checklist.md
│   ├── csharp.md
│   ├── css-less-sass.md
│   ├── django.md
│   ├── go.md
│   ├── java.md
│   ├── kotlin.md
│   ├── nestjs.md
│   ├── performance-review-guide.md
│   ├── python.md
│   ├── react.md
│   ├── rust.md
│   ├── security-review-guide.md
│   ├── svelte.md
│   ├── typescript.md
│   └── vue.md
├── scripts/
│   └── pr-analyzer.py
└── assets/
```

### Mapping

| Upstream Path | Local Folder | Notes |
|---|---|---|
| `SKILL.md` (root) | `rc-code-review/SKILL.md` | |
| `reference/*.md` | `rc-code-review/reference/*.md` | Our local `references/` folder may use different names — check on sync |
| `scripts/pr-analyzer.py` | `rc-code-review/scripts/pr-analyzer.py` | |

### API endpoints for awesome-skills/code-review-skill

```powershell
# List root files
gh api repos/awesome-skills/code-review-skill/contents --jq '.[].name'

# List reference files
gh api repos/awesome-skills/code-review-skill/contents/reference --jq '.[].name'

# Fetch SKILL.md
gh api repos/awesome-skills/code-review-skill/contents/SKILL.md --jq '.content' | base64 -d

# Fetch a reference file
gh api repos/awesome-skills/code-review-skill/contents/reference/typescript.md --jq '.content' | base64 -d
```

---

## Local-only Skills (no upstream — never diff)

These skills exist only in this repo and have no upstream counterpart:

| Local Folder | Origin |
|---|---|
| `rc-codeprobe` | Built from NishilBhave blog post — no public upstream repo |
| `rc-codeprobe-architecture` | Same |
| `rc-codeprobe-code-smells` | Same |
| `rc-codeprobe-error-handling` | Same |
| `rc-codeprobe-framework` | Same |
| `rc-codeprobe-patterns` | Same |
| `rc-codeprobe-performance` | Same |
| `rc-codeprobe-security` | Same |
| `rc-codeprobe-solid` | Same |
| `rc-codeprobe-testing` | Same |
| `rc-find-skills` | rc-specific |
| `rc-session-summary-prompt` | rc-specific |
| `rc-skill-updater` | This skill itself |

> **Note on `find-skills` and `session-summary-prompt`**: These are not present in the mattpocock upstream — verify if they were added upstream before treating as local-only.
