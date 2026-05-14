---
name: rightcode-git-commit-push
description: Creates a local git commit and optionally pushes it using a bundled Python script that inspects changed files, builds a commit message from user input plus git metadata, and prompts for remote selection when needed. Use when the user wants a local-only commit/push flow, asks to commit and push without using model tokens, or mentions generated commit messages, remote selection, or scripted git automation.
disable-model-invocation: true
argument-hint: "[optional short summary]"
---

# Local Git Commit Push

Runs a bundled Python script so the commit and push flow happens locally in the user's shell instead of spending tokens on diff analysis.

The script:
- detects the current git repo automatically
- inspects changed and untracked files
- asks for a short user summary if one is not provided
- generates a conventional-style commit subject locally
- stages changes with `git add -A`
- commits locally
- pushes only if a remote exists
- asks the user which remote to use when multiple remotes exist

## Quick Start

From anywhere inside the target repo:

```bash
python skills/rightcode-git-commit-push/scripts/git_commit_push.py --message "short summary"
```

If no summary is passed, the script prompts for one.

## Options

```bash
python skills/rightcode-git-commit-push/scripts/git_commit_push.py --help
```

Useful flags:
- `--message "..."` to seed the commit message
- `--remote origin` to skip remote selection
- `--no-push` to commit locally only even if remotes exist
- `--dry-run` to preview the generated commit message and chosen remote without changing git state
- `--repo <path>` to target a specific repository

## Expected Flow

1. Run the script.
2. Review the detected changed files.
3. Accept or edit the generated commit subject.
4. Confirm the commit.
5. If remotes exist, choose one remote and confirm push.

If no remotes are configured, the script commits locally and exits cleanly.

## Notes

- Requires Python 3.8+ and git on PATH.
- Works on Windows, macOS, and Linux.
- Keeps all commit-message generation local to the script.