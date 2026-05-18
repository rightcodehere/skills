#!/usr/bin/env python3
"""
rc-skill-updater: check.py
Scans upstream sources, diffs against local, produces a report JSON + prints summary.

Works on Windows, macOS, and Linux — stdlib only, no pip installs needed.

Usage:
    python check.py
    python check.py --report-path /tmp/my-report.json

Prerequisites:
    gh CLI installed and authenticated to github.com:
        gh auth login --hostname github.com

    Python 3.8+  (pre-installed on macOS; ships with most Linux distros;
                  download from https://python.org on Windows)
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# ANSI colours — disabled automatically when stdout is not a TTY
# ─────────────────────────────────────────────────────────────────────────────
USE_COLOUR = sys.stdout.isatty()

# Enable ANSI on Windows (needed for cmd.exe / older PowerShell)
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        USE_COLOUR = False

def _c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOUR else text

def cyan(t):    return _c(t, "36")
def green(t):   return _c(t, "32")
def yellow(t):  return _c(t, "33")
def red(t):     return _c(t, "31")
def white(t):   return _c(t, "1")   # bold white
def dim(t):     return _c(t, "2")


# ─────────────────────────────────────────────────────────────────────────────
# gh helpers
# ─────────────────────────────────────────────────────────────────────────────
def _gh(*args: str) -> tuple[int, str]:
    """Run a gh command and return (returncode, stdout+stderr)."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = result.stdout.strip() if result.returncode == 0 else (result.stderr or result.stdout).strip()
    return result.returncode, output


def gh_api(path: str) -> tuple[int, str]:
    return _gh("api", "--hostname", "github.com", path)


def fetch_upstream(api_path: str) -> str | None:
    """Fetch a file via the GitHub Contents API and decode its base64 content."""
    rc, out = gh_api(f"{api_path}?jq=.content" if "?" not in api_path else api_path)
    # gh --jq flag is cleaner
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", ".content")
    if rc != 0:
        return None
    b64 = re.sub(r"\s", "", out)
    try:
        return base64.b64decode(b64).decode("utf-8")
    except Exception:
        return None


def list_dir_upstream(api_path: str) -> list[str] | None:
    """Return a list of item names in an upstream directory, or None on error."""
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", '[.[] | select(.type=="dir") | .name]')
    if rc != 0:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def list_files_upstream(api_path: str) -> list[str]:
    """Return names of all items (files + dirs) in an upstream directory."""
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", "[.[].name]")
    if rc != 0:
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Auth guard
# ─────────────────────────────────────────────────────────────────────────────
def check_auth() -> None:
    """Exit with a helpful message if gh is not authenticated to github.com."""
    from shutil import which
    if not which("gh"):
        print(red("✗ gh CLI not found."))
        print("  Install from https://cli.github.com then run:")
        print("    gh auth login --hostname github.com")
        sys.exit(1)

    rc, _ = _gh("auth", "status", "--hostname", "github.com")
    if rc != 0:
        print(red("✗ gh is not authenticated to github.com."))
        print()
        print("  Run:  gh auth login --hostname github.com")
        print()
        print("  NOTE: If gh is authenticated to a GHE instance you still need a")
        print("  separate github.com login. Use --hostname github.com on every call.")
        sys.exit(1)

    print(green("✓ gh authenticated to github.com"))


# ─────────────────────────────────────────────────────────────────────────────
# Skill mappings — mirrors SOURCES.md
# ─────────────────────────────────────────────────────────────────────────────
MATTPOCOCK_SKILLS = [
    {"cat": "engineering",  "up": "diagnose",                      "local": "rc-diagnose",                      "files": ["SKILL.md", "scripts/hitl-loop.template.sh"]},
    {"cat": "engineering",  "up": "grill-with-docs",               "local": "rc-grill-with-docs",               "files": ["SKILL.md", "ADR-FORMAT.md", "CONTEXT-FORMAT.md"]},
    {"cat": "engineering",  "up": "improve-codebase-architecture",  "local": "rc-improve-codebase-architecture",  "files": ["SKILL.md", "DEEPENING.md", "INTERFACE-DESIGN.md", "LANGUAGE.md"]},
    {"cat": "engineering",  "up": "prototype",                     "local": "rc-prototype",                     "files": ["SKILL.md", "LOGIC.md", "UI.md"]},
    {"cat": "engineering",  "up": "setup-matt-pocock-skills",      "local": "rc-setup-skills",                  "files": ["SKILL.md", "domain.md", "issue-tracker-github.md", "issue-tracker-gitlab.md", "issue-tracker-local.md", "triage-labels.md"]},
    {"cat": "engineering",  "up": "tdd",                           "local": "rc-tdd",                           "files": ["SKILL.md", "deep-modules.md", "interface-design.md", "mocking.md", "refactoring.md", "tests.md"]},
    {"cat": "engineering",  "up": "to-issues",                     "local": "rc-to-issues",                     "files": ["SKILL.md"]},
    {"cat": "engineering",  "up": "to-prd",                        "local": "rc-to-prd",                        "files": ["SKILL.md"]},
    {"cat": "engineering",  "up": "triage",                        "local": "rc-triage",                        "files": ["SKILL.md", "AGENT-BRIEF.md", "OUT-OF-SCOPE.md"]},
    {"cat": "engineering",  "up": "zoom-out",                      "local": "rc-zoom-out",                      "files": ["SKILL.md"]},
    {"cat": "productivity", "up": "caveman",                       "local": "rc-caveman",                       "files": ["SKILL.md"]},
    {"cat": "productivity", "up": "grill-me",                      "local": "rc-grill-me",                      "files": ["SKILL.md"]},
    {"cat": "productivity", "up": "handoff",                       "local": "rc-handoff",                       "files": ["SKILL.md"]},
    {"cat": "productivity", "up": "write-a-skill",                 "local": "rc-write-a-skill",                 "files": ["SKILL.md"]},
    {"cat": "misc",         "up": "git-guardrails-claude-code",    "local": "rc-git-guardrails",                "files": ["SKILL.md", "scripts/block-dangerous-git.sh"]},
    {"cat": "misc",         "up": "migrate-to-shoehorn",           "local": "rc-migrate-to-shoehorn",           "files": ["SKILL.md"]},
    {"cat": "misc",         "up": "scaffold-exercises",            "local": "rc-scaffold-exercises",            "files": ["SKILL.md"]},
    {"cat": "misc",         "up": "setup-pre-commit",              "local": "rc-setup-pre-commit",              "files": ["SKILL.md"]},
]

CODE_REVIEW_FILES = [
    "SKILL.md",
    "reference/angular.md",
    "reference/architecture-review-guide.md",
    "reference/code-quality-universal.md",
    "reference/code-review-best-practices.md",
    "reference/common-bugs-checklist.md",
    "reference/csharp.md",
    "reference/css-less-sass.md",
    "reference/django.md",
    "reference/go.md",
    "reference/java.md",
    "reference/kotlin.md",
    "reference/nestjs.md",
    "reference/performance-review-guide.md",
    "reference/python.md",
    "reference/react.md",
    "reference/rust.md",
    "reference/security-review-guide.md",
    "reference/svelte.md",
    "reference/typescript.md",
    "reference/vue.md",
    "scripts/pr-analyzer.py",
]

LOCAL_ONLY_SKILLS = [
    "rc-codeprobe",
    "rc-codeprobe-architecture",
    "rc-codeprobe-code-smells",
    "rc-codeprobe-error-handling",
    "rc-codeprobe-framework",
    "rc-codeprobe-patterns",
    "rc-codeprobe-performance",
    "rc-codeprobe-security",
    "rc-codeprobe-solid",
    "rc-codeprobe-testing",
    "rc-session-summary-prompt",
    "rc-find-skills",
    "rc-skill-updater",
]

# Skills intentionally skipped from the upstream scan
SKIP_UPSTREAM = {"edit-article", "obsidian-vault", "review", "writing-beats", "writing-fragments", "writing-shape"}
CATEGORIES_TO_SCAN = ["engineering", "productivity", "misc", "in-progress"]


# ─────────────────────────────────────────────────────────────────────────────
# Diff helpers
# ─────────────────────────────────────────────────────────────────────────────
def _normalise(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _rewrite_name_field(content: str, local_name: str) -> str:
    """Replace the name: frontmatter field with the local skill name to avoid spurious diffs."""
    return re.sub(r"(?m)^name:\s*.+$", f"name: {local_name}", content)


def diff_counts(upstream: str, local_text: str) -> tuple[int, int]:
    """Return (added_lines, deleted_lines) between upstream and local."""
    up_lines    = _normalise(upstream).splitlines()
    local_lines = _normalise(local_text).splitlines()
    added = deleted = 0
    for line in up_lines:
        if line not in local_lines:
            added += 1
    for line in local_lines:
        if line not in up_lines:
            deleted += 1
    return added, deleted


def compare_file(upstream_content: str, local_path: Path) -> dict | None:
    """
    Returns None        → unchanged
            {"new": True}       → file doesn't exist locally
            {"add": n, "del": n, "content": str} → changed
    """
    if not local_path.exists():
        return {"new": True, "add": 0, "del": 0}

    local_text = local_path.read_text(encoding="utf-8")
    if _normalise(upstream_content) == _normalise(local_text):
        return None

    add, dele = diff_counts(upstream_content, local_text)
    return {"new": False, "add": add, "del": dele, "content": upstream_content}


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1 — detect new upstream skills
# ─────────────────────────────────────────────────────────────────────────────
def find_new_skills(tracked_upstream_names: set[str]) -> list[dict]:
    print()
    print(cyan("Phase 1: Scanning upstream categories for new skills..."))

    new_skills = []
    for cat in CATEGORIES_TO_SCAN:
        names = list_dir_upstream(f"repos/mattpocock/skills/contents/skills/{cat}")
        if names is None:
            print(f"  {yellow('WARNING')}: could not list category '{cat}'")
            continue
        for name in names:
            if name in tracked_upstream_names or name in SKIP_UPSTREAM:
                continue
            files = list_files_upstream(f"repos/mattpocock/skills/contents/skills/{cat}/{name}")
            new_skills.append({
                "category":    cat,
                "upstream":    name,
                "wouldBecome": f"rc-{name}",
                "files":       files,
            })

    print(f"  Found {len(new_skills)} new upstream skill(s).")
    return new_skills


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2 — diff mapped skills
# ─────────────────────────────────────────────────────────────────────────────
def diff_mattpocock_skills(skills_root: Path) -> list[dict]:
    print()
    print(cyan("Phase 2: Diffing mapped skills against mattpocock/skills..."))

    results = []
    for m in MATTPOCOCK_SKILLS:
        print(f"  {m['local']}...", end="", flush=True)
        changed_files: list[dict] = []
        new_files:     list[str]  = []
        fetch_errors:  list[str]  = []

        for f in m["files"]:
            api_path = f"repos/mattpocock/skills/contents/skills/{m['cat']}/{m['up']}/{f}"
            content  = fetch_upstream(api_path)
            if content is None:
                fetch_errors.append(f)
                continue

            # Preserve the local name field so it never gets overwritten by the upstream name
            if f == "SKILL.md":
                content = _rewrite_name_field(content, m["local"])

            local_path = skills_root / m["local"] / Path(f)
            cmp = compare_file(content, local_path)
            if cmp is None:
                continue
            if cmp["new"]:
                new_files.append(f)
            else:
                changed_files.append({"file": f, "add": cmp["add"], "del": cmp["del"], "upContent": content})

        status = "CHANGED" if (changed_files or new_files) else "UNCHANGED"
        label  = yellow("CHANGED") if status == "CHANGED" else dim("UNCHANGED")
        print(f" {label}")

        results.append({
            "local":        m["local"],
            "upstream":     "mattpocock/skills",
            "upPath":       f"skills/{m['cat']}/{m['up']}",
            "status":       status,
            "changedFiles": changed_files,
            "newFiles":     new_files,
            "fetchErrors":  fetch_errors,
        })

    return results


def diff_code_review_skill(skills_root: Path) -> dict:
    print()
    print(cyan("Phase 2b: Diffing rc-code-review against awesome-skills/code-review-skill..."))

    changed_files: list[dict] = []
    new_files:     list[str]  = []
    fetch_errors:  list[str]  = []

    for f in CODE_REVIEW_FILES:
        print(f"  {f}...", end="", flush=True)
        api_path = f"repos/awesome-skills/code-review-skill/contents/{f}"
        content  = fetch_upstream(api_path)
        if content is None:
            print(f" {red('SKIP (fetch error)')}")
            fetch_errors.append(f)
            continue

        # Preserve the local name field so it never gets overwritten by the upstream name
        if f == "SKILL.md":
            content = _rewrite_name_field(content, "rc-code-review")

        local_path = skills_root / "rc-code-review" / Path(f)
        cmp = compare_file(content, local_path)
        if cmp is None:
            print(f" {dim('ok')}")
            continue
        if cmp["new"]:
            print(f" {green('NEW')}")
            new_files.append(f)
        else:
            add, dele = cmp["add"], cmp["del"]
            print(f" {yellow(f'CHANGED (+{add} / -{dele})')}")
            changed_files.append({"file": f, "add": add, "del": dele, "upContent": content})

    status = "CHANGED" if (changed_files or new_files) else "UNCHANGED"
    return {
        "local":        "rc-code-review",
        "upstream":     "awesome-skills/code-review-skill",
        "upPath":       "(root)",
        "status":       status,
        "changedFiles": changed_files,
        "newFiles":     new_files,
        "fetchErrors":  fetch_errors,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Print report
# ─────────────────────────────────────────────────────────────────────────────
def print_summary(new_skills: list, skill_results: list, report_path: Path, script_dir: Path) -> None:
    changed   = [s for s in skill_results if s["status"] == "CHANGED"]
    unchanged = [s for s in skill_results if s["status"] == "UNCHANGED"]
    errored   = [s for s in skill_results if s["fetchErrors"]]

    bar = white("━" * 53)
    print()
    print(bar)
    print(white(f"  Upstream Sync Report  ({datetime.now().strftime('%Y-%m-%d %H:%M')})"))
    print(bar)
    print()

    # New skills
    label = green(f"New Skills ({len(new_skills)})") if new_skills else dim(f"New Skills (0)")
    print(label)
    if not new_skills:
        print("  (none)")
    else:
        for s in new_skills:
            print(f"  upstream: skills/{s['category']}/{s['upstream']}  →  would become: {s['wouldBecome']}")
            print(f"  Files: {', '.join(s['files'])}")

    print()

    # Changed
    label = yellow(f"Changed Skills ({len(changed)})") if changed else dim(f"Changed Skills (0)")
    print(label)
    if not changed:
        print("  (none)")
    else:
        for c in changed:
            print(f"  {c['local']}")
            for f in c["changedFiles"]:
                print(f"    ~ {f['file']} (+{f['add']} / -{f['del']})")
            for f in c["newFiles"]:
                print(f"    + {f}  (new file upstream)")

    print()

    # Unchanged
    print(dim(f"Unchanged Skills ({len(unchanged)})"))
    print("  " + ", ".join(s["local"] for s in unchanged))

    # Fetch errors
    if errored:
        print()
        print(red(f"Fetch Errors — check auth / network ({len(errored)})"))
        for e in errored:
            print(f"  {e['local']}: {', '.join(e['fetchErrors'])}")

    print()
    print(dim(f"Local-only Skills (not checked)"))
    print("  " + ", ".join(LOCAL_ONLY_SKILLS))

    print()
    print(bar)
    print(f"Report saved: {report_path}")
    print()

    if changed or new_skills:
        apply_script = script_dir / "apply.py"
        print(cyan("To apply changes run:"))
        print(cyan(f'  python "{apply_script}" --report-path "{report_path}"'))


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Check upstream skills for changes.")
    parser.add_argument("--report-path", default="", help="Where to write report.json")
    args = parser.parse_args()

    # Paths
    script_dir  = Path(__file__).resolve().parent          # .../scripts/
    skills_root = (script_dir / ".." / "..").resolve()     # .../skills/

    report_path = Path(args.report_path) if args.report_path else (
        Path(tempfile.mkdtemp(prefix="rightskills-sync-")) / "report.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Auth
    check_auth()

    # Phase 1 — new skills
    tracked_names = {m["up"] for m in MATTPOCOCK_SKILLS}
    new_skills = find_new_skills(tracked_names)

    # Phase 2 — diffs
    skill_results = diff_mattpocock_skills(skills_root)
    skill_results.append(diff_code_review_skill(skills_root))

    # Save report
    report_obj = {
        "date":       datetime.now().strftime("%Y-%m-%d %H:%M"),
        "newSkills":  new_skills,
        "skills":     skill_results,
        "localOnly":  LOCAL_ONLY_SKILLS,
        "skillsRoot": str(skills_root),
    }
    report_path.write_text(json.dumps(report_obj, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    print_summary(new_skills, skill_results, report_path, script_dir)


if __name__ == "__main__":
    main()
