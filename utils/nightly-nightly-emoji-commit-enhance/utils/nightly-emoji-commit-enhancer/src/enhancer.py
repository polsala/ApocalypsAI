#!/usr/bin/env python3
"""Emoji Commit Enhancer utility.

Provides a function to prepend an appropriate emoji to a Git commit message
based on simple keyword detection.
"""

import sys
from typing import List

# Mapping of keywords to emojis. The first match wins.
EMOJI_MAP = {
    "fix": "🛠️",
    "bug": "🐛",
    "add": "➕",
    "remove": "❌",
    "delete": "❌",
    "refactor": "♻️",
    "docs": "📚",
    "test": "🧪",
    "performance": "⚡",
    "security": "🔒",
}

DEFAULT_EMOJI = "✨"


def select_emoji(message: str) -> str:
    """Return the first matching emoji based on keywords in *message*.

    The search is case‑insensitive and looks for the keyword anywhere in the
    message. If no keyword matches, the default emoji is returned.
    """
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def enhance_message(message: str) -> str:
    """Prepend an appropriate emoji to *message*.

    If the message already starts with an emoji (the same one we would add),
    the original message is returned unchanged to avoid double‑emoji clutter.
    """
    emoji = select_emoji(message)
    # Simple check: if the first character is an emoji we added, skip.
    if message and message[0] == emoji[0]:
        return message
    return f"{emoji} {message}"


def main(argv: List[str] = None) -> int:
    """CLI entry point.

    Usage: enhancer.py <commit-message>
    The message can be provided as a single quoted argument or as multiple
    words which will be joined with spaces.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: enhancer.py <commit-message>", file=sys.stderr)
        return 1
    message = " ".join(argv)
    print(enhance_message(message))
    return 0


if __name__ == "__main__":
    sys.exit(main())
