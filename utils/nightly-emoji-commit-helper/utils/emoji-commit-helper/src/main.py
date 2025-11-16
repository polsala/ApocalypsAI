#!/usr/bin/env python3
"""
emoji_commit_helper: Suggest an emoji for a git commit message.
"""

import sys
from typing import Dict

EMOJI_MAP: Dict[str, str] = {
    "bug": "🐛",
    "fix": "🐛",
    "feature": "✨",
    "add": "✨",
    "docs": "📚",
    "doc": "📚",
    "refactor": "🔧",
    "test": "✅",
    "tests": "✅",
    "performance": "🚀",
    "perf": "🚀",
    "chore": "🧹",
}

DEFAULT_EMOJI = "🤖"


def suggest_emoji(message: str) -> str:
    """Return an emoji based on the first matching keyword in the message."""
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m emoji_commit_helper \"commit message\"")
        sys.exit(1)
    message = " ".join(argv)
    emoji = suggest_emoji(message)
    print(f"{emoji} {message}")


if __name__ == "__main__":
    main()
