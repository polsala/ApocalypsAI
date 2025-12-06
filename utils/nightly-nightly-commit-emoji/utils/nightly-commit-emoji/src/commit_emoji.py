"""commit_emoji.py

A tiny utility that suggests an emoji for a Git commit message based on keyword matching.

Public API:
    suggest_emoji(message: str) -> str
    main() – CLI entry point
"""

import argparse
import sys
from typing import Dict, List

# Mapping of keywords (lower‑case) to emojis
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "error": "🐛",
    "add": "✨",
    "create": "✨",
    "new": "✨",
    "remove": "🗑️",
    "delete": "🗑️",
    "rm": "🗑️",
    "refactor": "🛠️",
    "clean": "🛠️",
    "test": "✅",
    "tests": "✅",
    "doc": "📚",
    "docs": "📚",
    "readme": "📚",
    "performance": "🚀",
    "speed": "🚀",
    "merge": "🔀",
    "ci": "🤖",
    "cd": "🤖",
    "pipeline": "🤖",
    "security": "🔒",
    "auth": "🔒",
}

DEFAULT_EMOJI = "🔧"

def suggest_emoji(message: str) -> str:
    """Return the first matching emoji for *message*.

    The function lower‑cases the message, splits it into words, and returns the emoji
    associated with the first keyword it encounters. If none match, ``DEFAULT_EMOJI``
    is returned.
    """
    words: List[str] = message.lower().split()
    for word in words:
        if word in KEYWORD_EMOJI_MAP:
            return KEYWORD_EMOJI_MAP[word]
    return DEFAULT_EMOJI

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Suggest an emoji for a Git commit message based on keyword matching."
    )
    parser.add_argument(
        "message",
        help="The commit message to analyse. Enclose in quotes if it contains spaces.",
    )
    return parser.parse_args(argv)

def main() -> None:
    args = _parse_args()
    emoji = suggest_emoji(args.message)
    print(emoji)

if __name__ == "__main__":
    # When executed as a script, behave like a CLI tool.
    main()
