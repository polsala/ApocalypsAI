#!/usr/bin/env python3
"""emoji_helper: suggest an emoji for a git commit message.

The module provides a simple CLI that prints an emoji based on the first
matching keyword in the supplied commit message.
"""

from __future__ import annotations
import sys
from typing import List

# Mapping of keywords to emojis. The first keyword found wins.
EMOJI_MAP = {
    "add": "✨",
    "feature": "✨",
    "fix": "🐛",
    "bug": "🐛",
    "remove": "🗑️",
    "delete": "🗑️",
    "refactor": "🔧",
    "docs": "📝",
    "doc": "📝",
    "test": "✅",
    "tests": "✅",
    "performance": "⚡",
    "speed": "⚡",
    "security": "🔒",
    "ci": "🤖",
    "style": "🎨",
    "merge": "🔀",
    "revert": "⏪",
}


def suggest_emoji(message: str) -> str:
    """Return an emoji based on the first matching keyword in *message*.

    The function lower‑cases the message, strips punctuation, and checks each
    word against :data:`EMOJI_MAP`. If no keyword matches, a generic light‑bulb
    emoji is returned.
    """
    words = [w.lower().strip(".,!?:;()[]{}") for w in message.split()]
    for word in words:
        if word in EMOJI_MAP:
            return EMOJI_MAP[word]
    return "💡"  # Default for generic improvements


def main(argv: List[str] | None = None) -> int:
    """Entry point for the CLI.

    * If no arguments are supplied, prints a usage hint and exits with code 2.
    * Otherwise prints ``<emoji> <original message>`` and exits with code 0.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(
            "Usage: python -m utils.emoji-commit-helper.src.emoji_helper \"<commit message>\""
        )
        return 2
    message = " ".join(argv)
    emoji = suggest_emoji(message)
    print(f"{emoji} {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
