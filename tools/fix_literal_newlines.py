#!/usr/bin/env python3
"""Fix files that were committed with literal \\n escapes instead of real newlines."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
}

MAX_BYTES = 2 * 1024 * 1024


def iter_files(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                yield Path(dirpath) / name


def is_text(data: bytes) -> bool:
    return b"\x00" not in data


def should_unescape(text: str) -> bool:
    literal_newlines = text.count("\\n")
    actual_newlines = text.count("\n")
    if literal_newlines < 3:
        return False
    if actual_newlines > 1:
        return False
    return True


def unescape_text(text: str) -> str:
    # Decode only common newline-related escapes to avoid corrupting content.
    return text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")


def process_file(path: Path, write: bool) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if len(data) > MAX_BYTES or not is_text(data):
        return False
    text = data.decode("utf-8", errors="replace")
    if not should_unescape(text):
        return False
    decoded = unescape_text(text)
    if decoded == text:
        return False
    if decoded.count("\n") <= text.count("\n"):
        return False
    if write:
        path.write_text(decoded, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fix files that contain literal \\n sequences instead of real newlines."
    )
    ap.add_argument(
        "paths",
        nargs="*",
        default=["react-webpage"],
        help="Root paths to scan (default: react-webpage)",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help="Write changes to disk (default: dry run)",
    )
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths]
    changed = []
    for path in iter_files(roots):
        if process_file(path, write=args.write):
            changed.append(path)

    if changed:
        print("Updated files:" if args.write else "Would update files:")
        for path in changed:
            print(path)
    else:
        print("No files matched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
