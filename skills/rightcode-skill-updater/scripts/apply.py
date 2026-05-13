#!/usr/bin/env python3
"""
rightcode-skill-updater: apply.py
Interactive sync — reads the report from check.py and applies selected updates.

Works on Windows, macOS, and Linux — stdlib only, no pip installs needed.

Usage:
    python apply.py --report-path <path printed by check.py>

Prerequisites:
    Run check.py first to generate the report.
    gh CLI must be authenticated to github.com:
        gh auth login --hostname github.com
"""

import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# ANSI colours
# ─────────────────────────────────────────────────────────────────────────────
USE_COLOUR = sys.stdout.isatty()

if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        USE_COLOUR = False

def _c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOUR else text

def cyan(t):   return _c(t, "36")
def green(t):  return _c(t, "32")
def yellow(t): return _c(t, "33")
def red(t):    return _c(t, "31")
def white(t):  return _c(t, "1")
def dim(t):    return _c(t, "2")


# ─────────────────────────────────────────────────────────────────────────────
# gh helpers
# ─────────────────────────────────────────────────────────────────────────────
def _gh(*args: str) -> tuple[int, str]:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = result.stdout.strip() if result.returncode == 0 else (result.stderr or result.stdout).strip()
    return result.returncode, output


def fetch_upstream_file(api_path: str) -> str | None:
    """Fetch and decode a file from the GitHub Contents API."""
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", ".content")
    if rc != 0:
        print(f"  {red('WARNING')}: could not fetch {api_path}: {out}")
        return None
    b64 = re.sub(r"\s", "", out)
    try:
        return base64.b64decode(b64).decode("utf-8")
    except Exception as exc:
        print(f"  {red('WARNING')}: base64 decode failed for {api_path}: {exc}")
        return None


def list_files_upstream(api_path: str) -> list[str]:
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", "[.[].name]")
    if rc != 0:
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []


def get_upstream_type(api_path: str) -> str:
    """Return 'dir', 'file', or '' if unknown."""
    rc, out = _gh("api", "--hostname", "github.com", api_path, "--jq", ".type")
    if rc != 0:
        return ""
    return out.strip('"').strip()


# ─────────────────────────────────────────────────────────────────────────────
# File writer
# ─────────────────────────────────────────────────────────────────────────────
def write_skill_file(skills_root: Path, local_folder: str, relative_path: str, content: str) -> None:
    """Write content to the local skill file, creating parent dirs as needed."""
    full_path = skills_root / local_folder / Path(relative_path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")
    print(f"  {green('Written')}: {full_path.resolve()}")


# ─────────────────────────────────────────────────────────────────────────────
# Prompt helpers
# ─────────────────────────────────────────────────────────────────────────────
def ask(prompt: str, valid: tuple[str, ...] = ("y", "n")) -> str:
    while True:
        try:
            ans = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if not valid or ans in valid:
            return ans
        print(f"  Please enter one of: {', '.join(valid)}")


# ─────────────────────────────────────────────────────────────────────────────
# Apply changed skills
# ─────────────────────────────────────────────────────────────────────────────
def apply_changed(skills_root: Path, skill: dict) -> None:
    print(yellow(f"── {skill['local']} [{skill['upstream']}] ──"))
    for f in skill["changedFiles"]:
        print(f"   ~ {f['file']} (+{f['add']} / -{f['del']})")
    for f in skill["newFiles"]:
        print(f"   + {f}  (new file)")

    ans = ask(f"Apply changes to {skill['local']}? [y/n/file-by-file]: ", ("y", "n", "file-by-file"))

    def _new_file_api_path(up_path: str, f: str) -> str:
        if up_path == "(root)":
            return f"repos/{skill['upstream']}/contents/{f}"
        return f"repos/{skill['upstream']}/contents/{up_path}/{f}"

    if ans == "y":
        for f in skill["changedFiles"]:
            write_skill_file(skills_root, skill["local"], f["file"], f["upContent"])
        for f in skill["newFiles"]:
            api_path = _new_file_api_path(skill["upPath"], f)
            content  = fetch_upstream_file(api_path)
            if content is not None:
                write_skill_file(skills_root, skill["local"], f, content)

    elif ans == "file-by-file":
        for f in skill["changedFiles"]:
            fa = ask(f"  Apply {f['file']} (+{f['add']} / -{f['del']})? [y/n]: ")
            if fa == "y":
                write_skill_file(skills_root, skill["local"], f["file"], f["upContent"])
        for f in skill["newFiles"]:
            fa = ask(f"  Add new file {f}? [y/n]: ")
            if fa == "y":
                api_path = _new_file_api_path(skill["upPath"], f)
                content  = fetch_upstream_file(api_path)
                if content is not None:
                    write_skill_file(skills_root, skill["local"], f, content)

    else:
        print(dim("  Skipped."))

    print()


# ─────────────────────────────────────────────────────────────────────────────
# Add new skills
# ─────────────────────────────────────────────────────────────────────────────
def add_new_skill(skills_root: Path, skill: dict) -> None:
    cat, up   = skill["category"], skill["upstream"]
    local     = skill["wouldBecome"]
    files     = skill["files"]

    print(green(f"── NEW: {local}  [upstream: skills/{cat}/{up}] ──"))
    print(f"   Files: {', '.join(files)}")

    ans = ask(f"Add {local}? [y/n]: ")
    if ans != "y":
        print(dim("  Skipped."))
        print()
        return

    for entry in files:
        api_path = f"repos/mattpocock/skills/contents/skills/{cat}/{up}/{entry}"
        entry_type = get_upstream_type(api_path)

        if entry_type == "dir":
            # Recurse one level into the subdirectory
            sub_files = list_files_upstream(api_path)
            for sf in sub_files:
                sf_api = f"repos/mattpocock/skills/contents/skills/{cat}/{up}/{entry}/{sf}"
                content = fetch_upstream_file(sf_api)
                if content is not None:
                    write_skill_file(skills_root, local, f"{entry}/{sf}", content)
        else:
            content = fetch_upstream_file(api_path)
            if content is None:
                continue
            # Rewrite name: field in SKILL.md frontmatter to match local convention
            if entry == "SKILL.md":
                content = re.sub(r"(?m)^name:\s*.+$", f"name: {local}", content)
            write_skill_file(skills_root, local, entry, content)

    print()
    print(yellow(f"  REMINDER: Add a row to skills/rightcode-skill-updater/SOURCES.md for '{local}'."))
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Apply upstream skill updates interactively.")
    parser.add_argument("--report-path", required=True, help="Path to report.json produced by check.py")
    args = parser.parse_args()

    report_path = Path(args.report_path)
    if not report_path.exists():
        print(red(f"✗ Report not found: {report_path}"))
        print("  Run check.py first.")
        sys.exit(1)

    report = json.loads(report_path.read_text(encoding="utf-8"))

    # Resolve skills root
    skills_root_str = report.get("skillsRoot", "")
    skills_root = Path(skills_root_str) if skills_root_str and Path(skills_root_str).exists() else (
        Path(__file__).resolve().parent / ".." / ".."
    ).resolve()

    changed    = [s for s in report["skills"] if s["status"] == "CHANGED"]
    new_skills = report.get("newSkills", [])

    if not changed and not new_skills:
        print(green("Nothing to apply — all skills are up to date."))
        sys.exit(0)

    print()
    print(cyan(f"Sync report from: {report['date']}"))
    print(f"Skills root:      {skills_root}")
    print()

    # Apply changed skills
    for skill in changed:
        apply_changed(skills_root, skill)

    # Add new skills
    for skill in new_skills:
        add_new_skill(skills_root, skill)

    # Done
    bar = white("━" * 53)
    print(bar)
    print(cyan("Done. Review the changes above before committing."))
    print(cyan("Run your linter on any modified SKILL.md files."))


if __name__ == "__main__":
    main()
