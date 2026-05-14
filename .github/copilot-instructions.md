# RightSkills — Repo Instructions

This repo is the source for the `@rightcode/skills` npm package — a collection of agent skills for GitHub Copilot, Claude Code, Cursor, and compatible agent hosts.

---

## Repo structure

```
skills/
  rightcode-<name>/
    SKILL.md          # required — main skill instructions
    *.md              # optional reference/example files
    scripts/          # optional utility scripts (Python only — see below)
package.json          # npm package manifest
scripts/
  publish.ps1         # bump version + npm publish
  test-local.ps1      # install skills locally for testing
.github/
  workflows/
    publish.yml       # CI publish on git tag push
```

Each skill folder name **must** be prefixed with `rightcode-` and match the `name` field in the SKILL.md frontmatter.

Every new skill **must** also be added to `.claude-plugin/plugin.json` under the `skills` array:

```json
"./skills/rightcode-<name>"
```

---

## Creating a skill

Use the `rightcode-write-a-skill` skill as the starting point. The minimum required structure is:

```
skills/rightcode-<name>/
  SKILL.md
```

### SKILL.md frontmatter

```yaml
---
name: rightcode-<name>
description: <what it does>. Use when <specific triggers / keywords>.
---
```

**Description rules:**
- Max 1024 characters
- Write in third person
- First sentence: what capability it provides
- Second sentence: when/why to trigger it (keywords, contexts, file types)
- This is the only thing an agent sees when deciding whether to load the skill

### Adding reference files

If the skill content exceeds ~500 lines, split it into referenced files:

```
SKILL.md          # overview + links to reference files
REFERENCE.md      # detailed docs
EXAMPLES.md       # usage examples
```

---

## Script rules — Python only

Any utility scripts bundled inside a skill's `scripts/` folder **must be written in Python**.

**Rationale:** Python runs on Windows, macOS, and Linux without changes. Shell scripts (`.sh`, `.ps1`, `.bat`) are OS-specific and break on other platforms.

```
# Correct
skills/rightcode-<name>/scripts/helper.py

# Not allowed
skills/rightcode-<name>/scripts/helper.sh
skills/rightcode-<name>/scripts/helper.ps1
skills/rightcode-<name>/scripts/helper.bat
```

Scripts in the top-level `scripts/` folder (repo tooling, not skill content) are exempt — those are PowerShell because they only run on the maintainer's machine.

---

## Testing a skill locally (before publishing)

Use `test-local.ps1` to copy skills directly into `~/.agents/skills/` where VS Code and other agent hosts pick them up.

```powershell
# Install a single skill
.\scripts\test-local.ps1 rightcode-tdd

# Install multiple skills
.\scripts\test-local.ps1 rightcode-tdd rightcode-diagnose

# Install all skills
.\scripts\test-local.ps1

# Via npm script
npm run test:local -- rightcode-tdd
```

After running the script, reload VS Code (open a new chat) to pick up the changes. Iterate until the skill behaves correctly before moving to publish.

---

## Publishing

### Manual publish (local)

```powershell
.\scripts\publish.ps1
```

This bumps the patch version (`npm version patch`) and publishes to npm. Requires a valid `NODE_AUTH_TOKEN` in a `.env` file at the repo root (not committed).

### CI publish (GitHub Actions)

Push a version tag to trigger the automated publish workflow:

```powershell
git tag v1.2.3
git push origin v1.2.3
```

The workflow at `.github/workflows/publish.yml` publishes via npm OIDC trusted publishing — no token needed in CI.

---

## Workflow summary

```
create / edit skill
       ↓
.\scripts\test-local.ps1 <skill-name>
       ↓
test in VS Code chat
       ↓
iterate until correct
       ↓
git commit + push
       ↓
.\scripts\publish.ps1  (or tag for CI)
```
