#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def apply_diff(diff_path: Path) -> None:
    if not diff_path.exists():
        print(f"ERROR: Diff file not found: {diff_path}", file=sys.stderr)
        sys.exit(1)
    content = diff_path.read_text(encoding="utf-8")
    if not content.strip():
        print(f"ERROR: Diff file {diff_path} is empty.", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        ["git", "apply", "--whitespace=fix", str(diff_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR: Failed to apply diff:", file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a unified diff using git apply.")
    parser.add_argument("diff", help="Path to the unified diff file")
    args = parser.parse_args()
    apply_diff(Path(args.diff))


if __name__ == "__main__":
    main()
