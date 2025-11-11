"""emoji_helper.py

Utility to suggest an emoji for a Git commit message based on simple keyword matching.

The module provides:
- `get_emoji_for_message(message: str) -> str`: Returns the emoji string.
- CLI entry point when executed as a script.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Mapping of keyword groups to emojis. Order matters – first match wins.
_EMOJI_MAP: List[Tuple[Tuple[str, ...], str]] = [
    (("fix", "bug", "patch", "error", "mistake"), "🐛"),
    (("add", "feature", "implement", "create", "new"), "✨"),
    (("remove", "delete", "cleanup", "refactor", "rework"), "🗑️"),
    (("docs", "readme", "doc", "documentation"), "📚"),
    (("test", "tests", "testing"), "✅"),
]

_DEFAULT_EMOJI = "🔧"


def _normalize(text: str) -> List[str]:
    """Lower‑case and split a string into words.

    Simple tokenisation sufficient for our lightweight use‑case.
    """
    return text.lower().split()


def get_emoji_for_message(message: str) -> str:
    """Return an emoji that best matches the commit *message*.

    The function scans the message for any keyword in the predefined groups.
    The first matching group determines the emoji. If no keywords are found,
    a generic wrench ``🔧`` is returned.
    """
    words = set(_normalize(message))
    for keywords, emoji in _EMOJI_MAP:
        if any(keyword in words for keyword in keywords):
            return emoji
    return _DEFAULT_EMOJI


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="emoji-commit-helper",
        description="Suggest an emoji prefix for a Git commit message.",
    )
    parser.add_argument("message", nargs="+", help="Commit message (will be joined with spaces)")
    args = parser.parse_args()
    message = " ".join(args.message)
    emoji = get_emoji_for_message(message)
    # Print the emoji followed by the original message for convenience.
    print(f"{emoji} {message}")


if __name__ == "__main__":
    # When executed as a script, act as a CLI.
    _cli()
