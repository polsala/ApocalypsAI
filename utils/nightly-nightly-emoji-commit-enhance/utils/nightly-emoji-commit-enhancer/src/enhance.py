#!/usr/bin/env python3
"""
emoji_commit_enhancer: Append context‑aware emoji to a git commit message.
"""

import argparse
import random
import sys
from typing import List

# Mapping of keyword tuples to their representative emoji
_KEYWORD_MAP = {
    ("fix", "bug", "patch"): "🐛",
    ("add", "feature", "implement"): "✨",
    ("remove", "delete", "rm"): "❌",
}

# Fallback emojis used when no keyword matches
_RANDOM_EMOJIS = ["🎉", "🚀", "🤖"]


def _select_emoji(message: str) -> str:
    """Select an emoji based on simple keyword heuristics.

    If none of the defined keywords are present, a random celebratory emoji
    from ``_RANDOM_EMOJIS`` is returned.
    """
    lowered = message.lower()
    for keywords, emoji in _KEYWORD_MAP.items():
        if any(k in lowered for k in keywords):
            return emoji
    # No keyword matched; pick random celebratory emoji
    return random.choice(_RANDOM_EMOJIS)


def enhance_message(message: str) -> str:
    """Return the original message with a trailing emoji.

    Whitespace at the end of *message* is stripped before the emoji is added.
    """
    emoji = _select_emoji(message)
    return f"{message.rstrip()} {emoji}"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Append an emoji to a git commit message."
    )
    parser.add_argument("message", help="The commit message to enhance")
    args = parser.parse_args(argv)

    enhanced = enhance_message(args.message)
    print(enhanced)
    return 0


if __name__ == "__main__":
    sys.exit(main())
