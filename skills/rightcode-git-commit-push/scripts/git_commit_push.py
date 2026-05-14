from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChangedFile:
    code: str
    path: str


STATUS_LABELS = {
    "A": "added",
    "M": "modified",
    "D": "deleted",
    "R": "renamed",
    "C": "copied",
    "U": "updated",
    "?": "untracked",
}


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if check and process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or process.stdout.strip() or "git command failed")
    return process


def resolve_repo(path_value: str | None) -> Path:
    start_path = Path(path_value).resolve() if path_value else Path.cwd()
    probe = start_path if start_path.is_dir() else start_path.parent
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=probe,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if process.returncode != 0:
        raise RuntimeError("not inside a git repository")
    return Path(process.stdout.strip()).resolve()


def parse_status(repo: Path) -> list[ChangedFile]:
    output = run_git(repo, "status", "--porcelain=v1").stdout.splitlines()
    files: list[ChangedFile] = []
    for line in output:
        if not line:
            continue
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(ChangedFile(code=code, path=path))
    return files


def current_branch(repo: Path) -> str:
    process = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    return process.stdout.strip()


def list_remotes(repo: Path) -> list[str]:
    output = run_git(repo, "remote").stdout.splitlines()
    return [line.strip() for line in output if line.strip()]


def prompt(message: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{message}{suffix}: ").strip()
    if value:
        return value
    if default is not None:
        return default
    return ""


def confirm(message: str, default: bool = True) -> bool:
    options = "Y/n" if default else "y/N"
    while True:
        value = input(f"{message} [{options}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer y or n.")


def choose_remote(remotes: list[str], requested_remote: str | None) -> str | None:
    if requested_remote:
        if requested_remote not in remotes:
            raise RuntimeError(f"remote '{requested_remote}' was not found")
        return requested_remote
    if not remotes:
        return None
    if len(remotes) == 1:
        return remotes[0]
    print("Available remotes:")
    for index, remote in enumerate(remotes, start=1):
        print(f"  {index}. {remote}")
    while True:
        selection = prompt("Choose remote number")
        if selection.isdigit():
            value = int(selection)
            if 1 <= value <= len(remotes):
                return remotes[value - 1]
        print("Enter a valid remote number.")


def normalize_summary(summary: str) -> str:
    cleaned = re.sub(r"\s+", " ", summary).strip()
    cleaned = cleaned.rstrip(".!")
    if not cleaned:
        return "update changed files"
    return cleaned[0].lower() + cleaned[1:] if len(cleaned) > 1 else cleaned.lower()


def infer_commit_type(summary: str, files: list[ChangedFile]) -> str:
    lowered = summary.lower()
    keyword_map = {
        "fix": "fix",
        "bug": "fix",
        "repair": "fix",
        "docs": "docs",
        "readme": "docs",
        "test": "test",
        "refactor": "refactor",
        "cleanup": "refactor",
        "ci": "ci",
        "build": "build",
        "release": "chore",
        "bump": "chore",
        "add": "feat",
        "create": "feat",
        "implement": "feat",
    }
    for keyword, commit_type in keyword_map.items():
        if keyword in lowered:
            return commit_type

    paths = [item.path.lower() for item in files]
    if paths and all(path.endswith((".md", ".mdx", ".txt")) or "docs/" in path for path in paths):
        return "docs"
    if paths and all("test" in path or "spec" in path for path in paths):
        return "test"
    if any(path.startswith(".github/") for path in paths):
        return "ci"
    if any(path in {"package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"} for path in paths):
        return "build"
    return "chore"


def infer_scope(files: list[ChangedFile]) -> str | None:
    if not files:
        return None
    scopes: set[str] = set()
    for item in files:
        parts = Path(item.path).parts
        if len(parts) > 1:
            scopes.add(parts[0])
        else:
            scopes.add(Path(item.path).stem)
    if len(scopes) != 1:
        return None
    scope = next(iter(scopes)).lower()
    sanitized = re.sub(r"[^a-z0-9_-]+", "-", scope).strip("-")
    return sanitized or None


def build_commit_subject(summary: str, files: list[ChangedFile]) -> str:
    normalized = normalize_summary(summary)
    commit_type = infer_commit_type(normalized, files)
    scope = infer_scope(files)
    prefix = f"{commit_type}({scope}): " if scope else f"{commit_type}: "
    subject = prefix + normalized
    if len(subject) <= 72:
        return subject
    allowed = max(20, 72 - len(prefix) - 3)
    return prefix + normalized[:allowed].rstrip() + "..."


def build_commit_body(files: list[ChangedFile]) -> str | None:
    if not files:
        return None
    lines = ["Changed files:"]
    for item in files[:20]:
        labels = [STATUS_LABELS.get(char, "changed") for char in item.code if char != " "]
        label = "/".join(dict.fromkeys(labels)) if labels else "changed"
        lines.append(f"- {label}: {item.path}")
    remaining = len(files) - 20
    if remaining > 0:
        lines.append(f"- ... and {remaining} more")
    return "\n".join(lines)


def print_change_summary(files: list[ChangedFile]) -> None:
    print("Detected changes:")
    for item in files:
        print(f"  {item.code} {item.path}")


def stage_all(repo: Path) -> None:
    run_git(repo, "add", "-A")


def has_staged_changes(repo: Path) -> bool:
    process = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return process.returncode == 1


def create_commit(repo: Path, subject: str, body: str | None) -> None:
    args = ["commit", "-m", subject]
    if body:
        args.extend(["-m", body])
    run_git(repo, *args)


def push_commit(repo: Path, remote: str, branch: str) -> None:
    run_git(repo, "push", "-u", remote, branch)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a local git commit and optionally push it.")
    parser.add_argument("summary", nargs="*", help="Optional short user summary for the commit message")
    parser.add_argument("--message", help="Optional short user summary for the commit message")
    parser.add_argument("--repo", help="Path inside the target git repository")
    parser.add_argument("--remote", help="Remote name to push to")
    parser.add_argument("--no-push", action="store_true", help="Commit locally only")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without changing git state")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo = resolve_repo(args.repo)
        files = parse_status(repo)
        if not files:
            print("No changed or untracked files found.")
            return 0

        summary_seed = args.message or " ".join(args.summary).strip()
        if not summary_seed:
            summary_seed = prompt("Enter a short summary for this change")

        branch = current_branch(repo)
        remotes = list_remotes(repo)
        selected_remote = None if args.no_push else choose_remote(remotes, args.remote)
        subject = build_commit_subject(summary_seed, files)
        body = build_commit_body(files)

        print(f"Repository: {repo}")
        print(f"Branch: {branch}")
        print_change_summary(files)
        print(f"Suggested commit subject: {subject}")
        if body:
            print(body)

        choice = prompt("Accept subject, edit it, or cancel? [accept/edit/cancel]", "accept").lower()
        if choice == "cancel":
            print("Cancelled.")
            return 1
        if choice == "edit":
            subject = prompt("Enter commit subject", subject)

        if args.dry_run:
            if selected_remote:
                print(f"Dry run: would push to remote '{selected_remote}'.")
            else:
                print("Dry run: no remote push would happen.")
            return 0

        if not confirm("Stage all changes and create the commit?", True):
            print("Cancelled.")
            return 1

        stage_all(repo)
        if not has_staged_changes(repo):
            print("No stageable changes found after git add -A.")
            return 1

        create_commit(repo, subject, body)
        print("Commit created successfully.")

        if not selected_remote:
            print("No remotes configured. Commit was created locally only.")
            return 0

        if branch == "HEAD":
            print("Detached HEAD detected. Commit was created locally; skipping push.")
            return 0

        if not confirm(f"Push to remote '{selected_remote}' on branch '{branch}'?", True):
            print("Push skipped. Commit remains local.")
            return 0

        push_commit(repo, selected_remote, branch)
        print(f"Pushed to {selected_remote}/{branch}.")
        return 0
    except KeyboardInterrupt:
        print("Cancelled.")
        return 1
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())