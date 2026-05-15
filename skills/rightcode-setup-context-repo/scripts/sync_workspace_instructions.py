#!/usr/bin/env python3
"""One-way sync: context repo copilot-instructions.md -> workspace root."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy the context repository copilot-instructions.md to the workspace root "
            "as a one-way sync operation."
        )
    )
    parser.add_argument(
        "--context-repo",
        required=True,
        help="Path to the context repository root.",
    )
    parser.add_argument(
        "--workspace-root",
        required=True,
        help="Path to the workspace root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context_repo = Path(args.context_repo).resolve()
    workspace_root = Path(args.workspace_root).resolve()

    source = context_repo / "copilot-instructions.md"
    target = workspace_root / "copilot-instructions.md"

    if not source.exists():
        print(f"ERROR: Source file not found: {source}")
        return 2

    if not source.is_file():
        print(f"ERROR: Source is not a file: {source}")
        return 2

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    print("Synced workspace instructions")
    print(f"  source: {source}")
    print(f"  target: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
