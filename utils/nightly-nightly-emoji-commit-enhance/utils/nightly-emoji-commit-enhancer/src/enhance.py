#!/usr/bin/env python3
"""
emoji_commit_enhancer

Provides `enhance_message` to prepend an emoji based on keyword detection.
Can be used as a library or via CLI.
"""

import argparse
import sys
from typing import Dict

# Mapping of keyword to emoji
EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "add": "✨",
    "create": "✨",
    "remove": "🗑️",
    "delete": "🗑️",
    "docs": "📚",
    "doc": "📚",
    "refactor": "🔧",
    "test": "✅",
    "tests": "✅",
    "chore": "🔨",
    "perf": "⚡",
    "style": "🎨",
    "ci": "🤖",
    "build": "🏗️",
    "release": "🚀",
}


def enhance_message(message: str) -> str:
    """
    Prepend an appropriate emoji to ``message`` based on the first
    keyword that appears in the mapping. Matching is case‑insensitive
    and looks at whole words.

    If no keyword matches, returns the original message unchanged.
    """
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered.split():
            return f"{emoji} {message}"
    return message


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Prepend an emoji to a git commit message based on keywords."
    )
    parser.add_argument(
        "message",
        nargs="+",
        help="The commit message (will be joined with spaces).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv or sys.argv[1:])
    message = " ".join(args.message)
    enhanced = enhance_message(message)
    print(enhanced)


if __name__ == "__main__":
    main()
