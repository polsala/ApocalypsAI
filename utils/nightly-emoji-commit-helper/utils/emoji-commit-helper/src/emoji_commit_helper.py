#!/usr/bin/env python3
"""
emoji_commit_helper: Suggest an emoji prefix for a Git commit message based on keywords.
"""

import argparse
import sys
from typing import List, Tuple

# Mapping of keywords to emojis
KEYWORD_EMOJI_MAP: List[Tuple[str, str]] = [
    ("fix", "🐛"),
    ("bug", "🐛"),
    ("add", "✨"),
    ("feature", "✨"),
    ("remove", "🗑️"),
    ("delete", "🗑️"),
    ("refactor", "♻️"),
    ("docs", "📝"),
    ("test", "✅"),
    ("performance", "🚀"),
    ("security", "🔒"),
]

DEFAULT_EMOJI = "🔧"


def get_emoji(message: str) -> str:
    """
    Return the first matching emoji for the given commit message.
    Matching is case‑insensitive and looks for keyword substrings.
    """
    lowered = message.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP:
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="emoji-commit-helper",
        description="Suggest an emoji to prepend to a Git commit message.",
    )
    parser.add_argument(
        "message",
        nargs="+",
        help="Commit message (will be joined with spaces)",
    )
    args = parser.parse_args(argv)

    message = " ".join(args.message)
    emoji = get_emoji(message)
    print(f"{emoji} {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
