#!/usr/bin/env python3
"""
emoji-commit-enhancer

Provides a function to prepend an appropriate emoji to a git commit message.
"""

import argparse
import random
from typing import Dict

# Mapping of keyword to emoji
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "add": "➕",
    "remove": "➖",
    "delete": "🗑️",
    "refactor": "♻️",
    "docs": "📚",
    "doc": "📚",
    "test": "✅",
    "tests": "✅",
    "chore": "🔧",
    "perf": "⚡",
    "style": "🎨",
    "ci": "🤖",
    "build": "🏗️",
    "release": "🚀",
}

DEFAULT_EMOJIS = ["✨", "🚀", "🔥", "💡", "🎉"]


def choose_emoji(message: str) -> str:
    """Select an emoji based on keywords in the message, or a random default.

    Args:
        message: The original commit message.
    Returns:
        An emoji string.
    """
    lowered = message.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    # No keyword matched; pick a random default
    return random.choice(DEFAULT_EMOJIS)


def enhance_message(message: str) -> str:
    """Return the message prefixed with the chosen emoji.

    Args:
        message: The original commit message.
    Returns:
        The emoji‑enhanced commit message.
    """
    emoji = choose_emoji(message)
    return f"{emoji} {message}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepend an appropriate emoji to a git commit message."
    )
    parser.add_argument("message", help="The original commit message")
    args = parser.parse_args()
    print(enhance_message(args.message))


if __name__ == "__main__":
    main()
