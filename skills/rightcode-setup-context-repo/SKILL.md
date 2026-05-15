---
name: rightcode-setup-context-repo
description: Sets up a dedicated multi-repo context repository in a workspace, generates per-repo CONTEXT.md and ARCHITECTURE.md, and scaffolds project/repo standards plus instruction sync. Use when user wants a central onboarding context across multiple repos, asks for context map generation, or wants cross-repo Copilot instructions kept in sync.
disable-model-invocation: true
---

# Setup Context Repo

Create and maintain a dedicated `*-context` repository that centralizes domain language, architecture summaries, standards, and Copilot instruction policy across multiple repos in one workspace.

This is a prompt-driven skill. Explore first, then ask one decision at a time, then write.

## Required behavior

- Ask questions one at a time and wait for user confirmation.
- If a question can be answered by exploring the workspace, explore first.
- Prefer inferred defaults, then ask user to confirm.
- Use idempotent updates on re-run. Never destructively wipe generated content.

## Canonical defaults

Use these defaults unless user overrides:

- Create a new dedicated context repository (not per-repo context commits).
- Use nested repo folders inside the context repository.
- Suggest context repo name from common repo prefix with `-context` suffix, then ask user to confirm/edit.
- Generate `ARCHITECTURE.md` separately from `CONTEXT.md`.
- Generate standards in three tiers:
  - project-level standards (workspace-wide)
  - repo-level standards (stack-specific)
  - instruction-level policy (Copilot instruction docs)
- Detect existing standards using broad patterns and ask whether to merge or skip.
- Detect stack from config files first; if ambiguous, ask user.
- Create ADR folder skeleton only. Do not auto-create ADR documents.
- Update `.github/copilot-instructions.md` in every selected repo.
- Create workspace-level `copilot-instructions.md` in the context repository as the source of truth.
- Create a manual one-way sync script from context repository to workspace root.
- Default to soft enforcement (instruction + checklist). Offer optional hard enforcement toggle.
- Re-runs must update in place and preserve manual edits where possible.

## Discovery flow

### 1) Explore workspace and repos

Inspect workspace root and detect candidate repos:

- folder contains `.git`
- or folder has known stack files (`package.json`, `pyproject.toml`, `pom.xml`, `build.gradle`, `go.mod`, `Cargo.toml`, `*.csproj`, etc.)

Show detected repos and ask user which repos to include.

Default selection: include all detected repos, user can remove.

### 2) Suggest context repo name

Try common prefix detection from selected repo names.

- If prefix exists: propose `<prefix>-context`.
- If no prefix: propose `workspace-context` and ask for a better name.

Always ask user to confirm/edit.

### 3) Standards scope decisions

Ask separately:

- generate project-level standards? (yes/no)
- generate repo-level standards? (yes/no)

### 4) Enforcement decision

Use soft enforcement by default. Ask whether to also scaffold hard enforcement.

### 5) Existing standards scan

For each selected repo, scan broad patterns:

- `**/*STANDARDS*.md`
- `**/*standards*.md`
- `docs/**/standards*.md`
- `.github/**/standards*.md`

Summarize findings per repo and ask merge-or-skip.

## Generation flow

### 6) Build context repository structure

Create:

```text
<context-repo>/
  CONTEXT-MAP.md
  copilot-instructions.md
  docs/
    adr/
  scripts/
    sync_workspace_instructions.py
  PROJECT-STANDARDS.md                # optional
  CODING-STANDARDS.md                 # optional
  BRANCHING-STRATEGY.md               # optional
  TESTING-STANDARDS.md                # optional
  SECURITY-STANDARDS.md               # optional
  <repo-a>/
    CONTEXT.md
    ARCHITECTURE.md
    docs/
      adr/
    CODING-STANDARDS.md               # optional
    TESTING-STANDARDS.md              # optional
    SECURITY-STANDARDS.md             # optional
  <repo-b>/
    ...
```

### 7) Generate CONTEXT-MAP.md

Include:

- list of included repos with links/paths
- each repo role summary (frontend/backend/BFF/service/data/infra)
- cross-repo interactions
- ownership notes if known

### 8) Generate per-repo ARCHITECTURE.md

Infer from code/config first, then ask user to correct.

Each file must include:

- purpose
- tech stack
- role in system
- entry points
- external dependencies

### 9) Generate per-repo CONTEXT.md

Keep domain language separate from implementation details.

Use format compatible with grill-with-docs context rules:

- language terms with avoid aliases
- relationships
- example dialogue
- flagged ambiguities

### 10) Generate standards (if enabled)

- Pre-fill with practical defaults for detected stack.
- Use language/framework-aware baseline:
  - Java: package conventions, exception policy, testing stack, secure defaults
  - React/Next.js: component boundaries, data fetching, state, performance, security
  - Node backend: layering, validation, error handling, API contracts
  - Python/Django/FastAPI, Go, Rust, C#, etc.
- If stack is ambiguous, ask user before writing.

### 11) Update repo-level Copilot instructions

For each selected repo:

- create/update `.github/copilot-instructions.md`
- add section referencing context repository path
- add instruction that code changes must trigger related context updates
- include checklist guidance before commit

Do not remove existing user guidance. Merge in place.

### 12) Create workspace-level instruction source

Write `<context-repo>/copilot-instructions.md` containing:

- context repository location and purpose
- requirement to keep context files current
- coding standards, branching, testing, security references
- cross-repo architecture expectations
- guidance for updating standards when system evolves

### 13) Create sync script

Create `<context-repo>/scripts/sync_workspace_instructions.py`.

Behavior:

- source: `<context-repo>/copilot-instructions.md`
- target: `<workspace-root>/copilot-instructions.md`
- one-way copy (context repo is source of truth)
- create target if missing
- overwrite target on each run
- print clear status and exit codes

## Idempotent re-run policy

On re-run:

- re-scan repos and report new/removed repos
- add missing artifacts
- update generated sections in existing files
- preserve user-edited sections where possible
- if merge uncertainty exists, add clear conflict markers and ask user

Never delete user-authored content silently.

## Output report to user

After generation, summarize:

- selected repos
- created/updated files
- unresolved ambiguities
- whether hard enforcement was enabled
- command to run sync script

Then ask user to review generated artifacts before any commit operations.

## Guardrails

- Do not create ADR documents automatically.
- Do not force hard enforcement by default.
- Do not assume framework when stack detection is ambiguous.
- Do not flatten nested repo folders in context repository.
- Do not overwrite existing instruction files blindly.
