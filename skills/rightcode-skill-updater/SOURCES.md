# Upstream Sources

> **Verified against live repos on 2026-05-13.** Re-verify after major upstream changes.

Two upstream sources. The codeprobe sub-skills (`rightcode-codeprobe-*`) are **local-only** — they were inspired by the NishilBhave blog post (https://dev.to/nishilbhave/...) but have no public upstream repo to sync against.

---

## Source 1 — mattpocock/skills

**URL**: https://github.com/mattpocock/skills  
**Structure**: `skills/<category>/<skill-name>/SKILL.md` — skills are nested under category subfolders, **not** at a flat `skills/<name>/` level.

### Categories and skills

| Category | Upstream Skill Folder | Local Folder | Notes |
|---|---|---|---|
| `engineering` | `diagnose` | `rightcode-diagnose` | |
| `engineering` | `grill-with-docs` | `rightcode-grill-with-docs` | |
| `engineering` | `improve-codebase-architecture` | `rightcode-improve-codebase-architecture` | |
| `engineering` | `prototype` | `rightcode-prototype` | |
| `engineering` | `setup-matt-pocock-skills` | `rightcode-setup-skills` | Upstream name differs — we renamed |
| `engineering` | `tdd` | `rightcode-tdd` | |
| `engineering` | `to-issues` | `rightcode-to-issues` | |
| `engineering` | `to-prd` | `rightcode-to-prd` | |
| `engineering` | `triage` | `rightcode-triage` | |
| `engineering` | `zoom-out` | `rightcode-zoom-out` | |
| `productivity` | `caveman` | `rightcode-caveman` | |
| `productivity` | `grill-me` | `rightcode-grill-me` | |
| `productivity` | `handoff` | `rightcode-handoff` | |
| `productivity` | `write-a-skill` | `rightcode-write-a-skill` | |
| `misc` | `git-guardrails-claude-code` | `rightcode-git-guardrails` | Upstream name differs — we shortened |
| `misc` | `migrate-to-shoehorn` | `rightcode-migrate-to-shoehorn` | |
| `misc` | `scaffold-exercises` | `rightcode-scaffold-exercises` | |
| `misc` | `setup-pre-commit` | `rightcode-setup-pre-commit` | |

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
├── SKILL.md              ← root-level, tracks as: rightcode-code-review
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
| `SKILL.md` (root) | `rightcode-code-review/SKILL.md` | |
| `reference/*.md` | `rightcode-code-review/reference/*.md` | Our local `references/` folder may use different names — check on sync |
| `scripts/pr-analyzer.py` | `rightcode-code-review/scripts/pr-analyzer.py` | |

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
| `rightcode-codeprobe` | Built from NishilBhave blog post — no public upstream repo |
| `rightcode-codeprobe-architecture` | Same |
| `rightcode-codeprobe-code-smells` | Same |
| `rightcode-codeprobe-error-handling` | Same |
| `rightcode-codeprobe-framework` | Same |
| `rightcode-codeprobe-patterns` | Same |
| `rightcode-codeprobe-performance` | Same |
| `rightcode-codeprobe-security` | Same |
| `rightcode-codeprobe-solid` | Same |
| `rightcode-codeprobe-testing` | Same |
| `rightcode-find-skills` | RightCode-specific |
| `rightcode-session-summary-prompt` | RightCode-specific |
| `rightcode-skill-updater` | This skill itself |

> **Note on `find-skills` and `session-summary-prompt`**: These are not present in the mattpocock upstream — verify if they were added upstream before treating as local-only.
