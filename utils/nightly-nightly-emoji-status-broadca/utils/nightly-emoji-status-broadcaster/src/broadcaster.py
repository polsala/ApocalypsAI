"""emoji_status_broadcaster

Utility to map textual status identifiers to emojis and produce a human‑readable summary.

Provides both a library API and a tiny CLI.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List

# Mapping of canonical status keys to (emoji, pretty name)
_STATUS_MAP: Dict[str, tuple[str, str]] = {
    "success": ("✅", "Success"),
    "failure": ("❌", "Failure"),
    "in_progress": ("⏳", "In Progress"),
    "pending": ("🕒", "Pending"),
    "canceled": ("🚫", "Canceled"),
}

def _normalize(status: str) -> str:
    """Normalize a raw status string to the canonical key.

    The function lower‑cases the input and replaces spaces/hyphens with underscores.
    """
    return status.strip().lower().replace(" ", "_").replace("-", "_")

def status_to_emoji(status: str) -> str:
    """Return the emoji for *status*.

    If the status is unknown, returns the generic question‑mark emoji.
    """
    key = _normalize(status)
    emoji, _ = _STATUS_MAP.get(key, ("❓", status.title()))
    return emoji

def summarize_statuses(statuses: List[str]) -> str:
    """Create a comma‑separated summary of *statuses* with emojis.

    Example:
        >>> summarize_statuses(["success", "failure", "in_progress"])
        '✅ Success, ❌ Failure, ⏳ In Progress'
    """
    parts = []
    for s in statuses:
        key = _normalize(s)
        emoji, pretty = _STATUS_MAP.get(key, ("❓", s.title()))
        parts.append(f"{emoji} {pretty}")
    return ", ".join(parts)

def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="emoji-status-broadcaster",
        description="Convert status words to emojis and optionally summarize them.",
    )
    parser.add_argument(
        "statuses",
        nargs="+",
        help="One or more status strings (e.g. success failure in_progress).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a single comma‑separated summary instead of one emoji per line.",
    )
    return parser

def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)
    if args.summary:
        print(summarize_statuses(args.statuses))
    else:
        for s in args.statuses:
            print(status_to_emoji(s))
    return 0

if __name__ == "__main__":
    # When executed as a script, forward sys.argv[1:]
    sys.exit(main(sys.argv[1:]))
