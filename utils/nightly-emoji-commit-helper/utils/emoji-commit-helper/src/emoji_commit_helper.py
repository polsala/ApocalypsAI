"""
emoji_commit_helper.py

Provides a simple function to suggest an emoji based on commit message keywords.
"""

import sys
from typing import List, Tuple

# Simple keyword → emoji mapping (order matters: first match wins)
KEYWORD_EMOJI_MAP: List[Tuple[str, str]] = [
    ("feat", "✨"),
    ("feature", "✨"),
    ("add", "✨"),
    ("fix", "🐛"),
    ("bug", "🐛"),
    ("remove", "🗑️"),
    ("delete", "🗑️"),
    ("refactor", "🔧"),
    ("docs", "📝"),
    ("test", "✅"),
    ("ci", "🤖"),
    ("perf", "⚡"),
    ("style", "💄"),
    ("chore", "🔧"),
]


def suggest_emoji(message: str) -> str:
    """Return an emoji that best matches the commit message.

    The function lower‑cases the message and returns the emoji associated with the
    first keyword found in `KEYWORD_EMOJI_MAP`. If no keyword matches, a generic
    celebration emoji is returned.
    """
    lowered = message.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP:
        if keyword in lowered:
            return emoji
    return "🎉"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_commit_helper \"<commit message>\"")
        sys.exit(1)
    msg = sys.argv[1]
    emoji = suggest_emoji(msg)
    print(f"{emoji} {msg}")


if __name__ == "__main__":
    main()
