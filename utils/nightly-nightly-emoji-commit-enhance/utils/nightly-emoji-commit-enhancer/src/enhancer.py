"""Emoji Commit Enhancer utility.

Scans a commit message for known keywords and prefixes an appropriate emoji.
"""

import sys
from typing import List, Tuple

# Mapping of keyword (lowercase) to emoji.
_EMOJI_MAP: List[Tuple[str, str]] = [
    ("fix", "🐛"),
    ("bug", "🐛"),
    ("add", "➕"),
    ("create", "➕"),
    ("remove", "❌"),
    ("delete", "❌"),
    ("refactor", "♻️"),
    ("update", "🔄"),
    ("docs", "📝"),
    ("test", "✅"),
]


def enhance_message(message: str) -> str:
    """Return the message prefixed with an emoji if a keyword matches.

    The first keyword found (case‑insensitive) determines the emoji.
    If no keyword matches, the original message is returned unchanged.
    """
    lowered = message.lower()
    for keyword, emoji in _EMOJI_MAP:
        if keyword in lowered:
            return f"{emoji} {message}"
    return message


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Expects a single argument: the commit message.
    Prints the enhanced message to stdout.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Error: commit message required.", file=sys.stderr)
        return 1
    message = " ".join(argv)
    print(enhance_message(message))
    return 0


if __name__ == "__main__":
    sys.exit(main())
