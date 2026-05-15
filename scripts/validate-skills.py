#!/usr/bin/env python3
"""Validate skill authoring quality for this repository.

Checks implemented:
- Required skill structure and SKILL.md frontmatter keys.
- Folder name/frontmatter name/plugin registration consistency.
- Local markdown link integrity in SKILL.md.
- Python-only files under each skill's scripts/ directory.

Warnings (non-blocking):
- Description style heuristics (third-person and sentence count guidance).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote


# ---------------------------------------------------------------------------
# Colour helpers — only emit ANSI codes when stdout is a real terminal or the
# caller has set FORCE_COLOR (common in CI with colour support).
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_USE_COLOR = _supports_color()


class _C:
    RESET  = "\033[0m"  if _USE_COLOR else ""
    BOLD   = "\033[1m"  if _USE_COLOR else ""
    RED    = "\033[31m" if _USE_COLOR else ""
    GREEN  = "\033[32m" if _USE_COLOR else ""
    YELLOW = "\033[33m" if _USE_COLOR else ""
    CYAN   = "\033[36m" if _USE_COLOR else ""
    DIM    = "\033[2m"  if _USE_COLOR else ""


def _pass(text: str) -> str:
    return f"{_C.BOLD}{_C.GREEN}{text}{_C.RESET}"


def _fail(text: str) -> str:
    return f"{_C.BOLD}{_C.RED}{text}{_C.RESET}"


def _error(text: str) -> str:
    return f"{_C.RED}{text}{_C.RESET}"


def _warn(text: str) -> str:
    return f"{_C.YELLOW}{text}{_C.RESET}"


def _skill(text: str) -> str:
    return f"{_C.BOLD}{text}{_C.RESET}"


def _dim(text: str) -> str:
    return f"{_C.DIM}{text}{_C.RESET}"


# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"


@dataclass
class Finding:
    code: str
    message: str
    path: str


@dataclass
class SkillResult:
    skill: str
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


def run_git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = proc.stdout if proc.returncode == 0 else (proc.stderr or proc.stdout)
    return proc.returncode, output.strip()


def staged_files() -> list[str]:
    rc, out = run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    if rc != 0:
        return []
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def changed_skills_from_paths(paths: list[str]) -> list[str]:
    names: set[str] = set()
    for path in paths:
        if not path.startswith("skills/"):
            continue
        parts = path.split("/")
        if len(parts) >= 2 and parts[1]:
            names.add(parts[1])
    return sorted(names)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"\A---\n(.*?)\n---\n?", normalized, flags=re.DOTALL)
    if not match:
        return None

    data: dict[str, str] = {}
    for line in match.group(1).split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1).strip(), m.group(2).strip()
        data[key] = value
    return data


def is_probably_third_person(description: str) -> bool:
    return re.search(r"\b(i|me|my|mine|we|our|ours|you|your|yours)\b", description, flags=re.IGNORECASE) is None


def sentence_count(text: str) -> int:
    return len(re.findall(r"[^.!?]+[.!?]", text))


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def normalize_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target:
        return None

    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()

    target = target.split()[0]

    lowered = target.lower()
    if lowered.startswith(("http://", "https://", "mailto:", "#")):
        return None

    target = target.split("#", 1)[0].split("?", 1)[0]
    target = unquote(target)

    if not target.lower().endswith(".md"):
        return None

    return target


def load_plugin_skills() -> set[str]:
    if not PLUGIN_JSON.exists():
        return set()

    try:
        payload = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()

    skills = payload.get("skills", [])
    registered: set[str] = set()
    if isinstance(skills, list):
        for item in skills:
            if isinstance(item, str):
                normalized = item.replace("\\", "/")
                if normalized.startswith("./"):
                    normalized = normalized[2:]
                registered.add(normalized)
    return registered


def validate_skill(skill_name: str, registered_paths: set[str]) -> SkillResult:
    result = SkillResult(skill=skill_name)
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        result.errors.append(
            Finding(
                code="structure.missing-skill-md",
                message="Missing SKILL.md in skill folder.",
                path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
            )
        )
        return result

    text = skill_md.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)

    if frontmatter is None:
        result.errors.append(
            Finding(
                code="structure.invalid-frontmatter",
                message="SKILL.md must begin with YAML frontmatter delimited by ---.",
                path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
            )
        )
        return result

    fm_name = frontmatter.get("name", "").strip()
    if not fm_name:
        result.errors.append(
            Finding(
                code="structure.missing-name",
                message="Frontmatter must include a non-empty name field.",
                path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
            )
        )
    elif fm_name != skill_name:
        result.errors.append(
            Finding(
                code="naming.folder-name-mismatch",
                message=f"Frontmatter name '{fm_name}' must match folder name '{skill_name}'.",
                path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
            )
        )

    desc = frontmatter.get("description", "").strip()
    if not desc:
        result.errors.append(
            Finding(
                code="structure.missing-description",
                message="Frontmatter must include a non-empty description field.",
                path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
            )
        )
    else:
        if len(desc) > 1024:
            result.errors.append(
                Finding(
                    code="structure.description-too-long",
                    message=f"Description must be <= 1024 characters (found {len(desc)}).",
                    path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
                )
            )

        if not is_probably_third_person(desc):
            result.warnings.append(
                Finding(
                    code="style.description-third-person",
                    message="Description appears to use first/second-person language; prefer third person.",
                    path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
                )
            )

        if sentence_count(desc) < 2:
            result.warnings.append(
                Finding(
                    code="style.description-two-sentences",
                    message="Description should ideally have two sentences (capability, then trigger guidance).",
                    path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
                )
            )

    expected_plugin_entry = f"skills/{skill_name}"
    if expected_plugin_entry not in registered_paths:
        result.errors.append(
            Finding(
                code="naming.missing-plugin-registration",
                message=f"Missing plugin registration './{expected_plugin_entry}' in .claude-plugin/plugin.json.",
                path=".claude-plugin/plugin.json",
            )
        )

    for link in markdown_links(text):
        target = normalize_link_target(link)
        if target is None:
            continue

        if target.startswith("/"):
            resolved = ROOT / target.lstrip("/")
        else:
            resolved = skill_dir / target

        if not resolved.exists():
            result.errors.append(
                Finding(
                    code="references.broken-link",
                    message=f"Broken markdown link target '{target}'.",
                    path=str(skill_md.relative_to(ROOT)).replace("\\", "/"),
                )
            )

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for path in scripts_dir.rglob("*"):
            if not path.is_file():
                continue

            # Ignore common bytecode/cache artifacts; enforce source script policy.
            if "__pycache__" in path.parts or path.suffix.lower() in {".pyc", ".pyo"}:
                continue

            if path.suffix.lower() != ".py":
                result.errors.append(
                    Finding(
                        code="scripts.non-python-file",
                        message="Files under skills/*/scripts/ must be Python (.py).",
                        path=str(path.relative_to(ROOT)).replace("\\", "/"),
                    )
                )

    return result


def print_summary(mode: str, checked_skills: list[str], results: list[SkillResult]) -> None:
    print(f"{_dim('validate-skills')} mode={mode}")

    if not checked_skills:
        print(_dim("No changed skills detected; skipping validation."))
        return

    print()
    for result in results:
        label = _pass("[PASS]") if result.passed else _fail("[FAIL]")
        print(f"{label} {_skill(result.skill)}")
        for finding in result.errors:
            print(f"  {_error('ERROR')} {_dim(finding.code)} {finding.path}: {finding.message}")
        for finding in result.warnings:
            print(f"  {_warn('WARN ')} {_dim(finding.code)} {finding.path}: {finding.message}")

    errors = sum(len(r.errors) for r in results)
    warnings = sum(len(r.warnings) for r in results)
    failed = sum(1 for r in results if not r.passed)
    passed = len(results) - failed

    print()
    print(f"Skills checked : {len(results)}")
    print(f"Passed         : {_pass(str(passed))}")
    print(f"Failed         : {(_fail if failed else _pass)(str(failed))}")
    print(f"Errors         : {(_error if errors else _pass)(str(errors))}")
    print(f"Warnings       : {(_warn if warnings else _pass)(str(warnings))}")


def as_json(mode: str, checked_skills: list[str], results: list[SkillResult]) -> dict[str, Any]:
    errors = sum(len(r.errors) for r in results)
    warnings = sum(len(r.warnings) for r in results)
    failed = sum(1 for r in results if not r.passed)
    passed = len(results) - failed

    return {
        "mode": mode,
        "skillsChecked": checked_skills,
        "totals": {
            "skills": len(results),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "warnings": warnings,
        },
        "results": [
            {
                "skill": r.skill,
                "status": "pass" if r.passed else "fail",
                "errors": [e.__dict__ for e in r.errors],
                "warnings": [w.__dict__ for w in r.warnings],
            }
            for r in results
        ],
    }


def all_skills() -> list[str]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate RightSkills skill authoring quality.")
    parser.add_argument("--mode", choices=["all", "staged"], default="all")
    parser.add_argument("--json-out", help="Optional path for JSON report output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.mode == "staged":
        checked_skills = changed_skills_from_paths(staged_files())
    else:
        checked_skills = all_skills()

    registered_paths = load_plugin_skills()
    results = [validate_skill(name, registered_paths) for name in checked_skills]

    print_summary(args.mode, checked_skills, results)

    payload = as_json(args.mode, checked_skills, results)
    if args.json_out:
        out_path = Path(args.json_out)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"JSON report written to {out_path}")

    has_errors = any(r.errors for r in results)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
