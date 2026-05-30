---
name: rc-git-workflow
description: Applies a disciplined Git collaboration workflow with branch conventions, atomic commits, clean PRs, safe rebases, and branch lifecycle hygiene. Use when users ask for branching strategy, commit structure, PR preparation, conflict resolution, or team Git process standardization.
---

# Git Workflow

Use repeatable Git practices that keep history clear and delivery predictable.

## When to Use This Skill

Use this skill when the user asks to:

- Create or name branches consistently
- Structure commits using conventional semantics
- Prepare PRs with clear summaries and testing notes
- Resolve rebase conflicts safely
- Choose or refine team branching strategy

## Default Guidance

Prefer short-lived branches with small PRs and linear history.

## Workflow

### Step 1: Branch creation

Use branch prefixes:

- feat/
- fix/
- docs/
- refactor/
- chore/

### Step 2: Atomic commits

- One logical change per commit
- Imperative summary line
- Include scope when useful

### Step 3: PR preparation

- Keep PR size manageable
- Summarize what changed, why, and how tested
- Rebase/squash WIP commits before review

### Step 4: Merge and cleanup

- Merge only after green CI and review
- Delete merged branches
- Keep main protected

## Conflict handling quick path

```bash
git status
git add <resolved-files>
git rebase --continue
```

Abort if needed:

```bash
git rebase --abort
```

## Anti-patterns

- Direct commits to protected main
- Very large PRs with mixed concerns
- Merge commits used where linear history is required
- Long-lived stale branches

## Production Checklist

- [ ] Branch naming convention followed
- [ ] Commit messages are clear and scoped
- [ ] PR includes test evidence
- [ ] CI and review gates are enforced
- [ ] Branch cleanup performed after merge

## Sources

- Conventional Commits
- GitHub Flow and trunk-based development references
- Git official rebase and conflict-resolution docs
