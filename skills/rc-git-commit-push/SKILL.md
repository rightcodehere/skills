---
name: rc-git-commit-push
description: Creates a local git commit and optionally pushes it using a bundled Python script that inspects changed files, generates the commit message locally from git state, and supports a one-shot auto-approve mode. Use when the user wants a local-only commit/push flow, asks to commit and push without using model tokens, or mentions generated commit messages, remote selection, or scripted git automation.
disable-model-invocation: true
argument-hint: "[optional short summary]"
---

# Local Git Commit Push

Runs a bundled Python script so the commit and push flow happens locally in the user's shell instead of spending tokens on diff analysis.

Execution rules:
- Run the bundled Python script directly from the repo root or with `--repo`.
- Do not add planning text, tool-selection narration, or a fabricated execution transcript before running it.
- After the script finishes, report only the concrete outcome from the local command.
- If the user asked to commit only, pass `--no-push`.

The script:
- detects the current git repo automatically
- inspects changed and untracked files
- generates a conventional-style commit subject locally from the changed files when no message is provided
- stages changes with `git add -A`
- commits locally
- pushes only if a remote exists
- asks the user which remote to use when multiple remotes exist
- can skip commit and push confirmations with `--yes`

## Quick Start

From anywhere inside the target repo:

```bash
python skills/rc-git-commit-push/scripts/git_commit_push.py --yes
```

That runs the full local flow with an auto-generated subject and no confirmation prompts unless remote choice is ambiguous.

## Options

```bash
python skills/rc-git-commit-push/scripts/git_commit_push.py --help
```

Useful flags:
- `--message "..."` to seed the commit message
- `--remote origin` to skip remote selection
- `--no-push` to commit locally only even if remotes exist
- `--dry-run` to preview the generated commit message and chosen remote without changing git state
- `--repo <path>` to target a specific repository
- `--yes` to auto-accept the generated subject and skip commit/push confirmations

## Expected Flow

1. Run the script.
2. Review the detected changed files and generated subject.
3. If you did not pass `--yes`, optionally edit the subject.
4. If multiple remotes exist and `--remote` was not passed, choose one remote.

If no remotes are configured, the script commits locally and exits cleanly.

## Notes

- Requires Python 3.8+ and git on PATH.
- Works on Windows, macOS, and Linux.
- Keeps all commit-message generation local to the script.
