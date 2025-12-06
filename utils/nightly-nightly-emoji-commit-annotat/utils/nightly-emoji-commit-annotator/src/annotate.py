"""
emoji_commit_annotator

Provides a simple function to prepend an emoji to a git commit message
based on keyword heuristics, and a CLI entry point.
"""

import sys
from typing import Tuple

# Mapping of keyword to emoji
_KEYWORD_EMOJI_MAP = {
    "fix": "🛠️",
    "bug": "🐛",
    "add": "✨",
    "remove": "❌",
    "delete": "❌",
    "refactor": "♻️",
    "docs": "📚",
    "test": "✅",
    "performance": "⚡",
    "security": "🔒",
}


def _find_keyword(message: str) -> Tuple[str, str]:
    """
    Return the first matching keyword and its emoji.
    Search is case‑insensitive.
    """
    lowered = message.lower()
    for kw, emoji in _KEYWORD_EMOJI_MAP.items():
        if kw in lowered:
            return kw, emoji
    return "", "🔧"  # fallback emoji


def annotate(message: str) -> str:
    """
    Prepend an appropriate emoji to *message*.

    Parameters
    ----------
    message: str
        The original git commit message.

    Returns
    -------
    str
        Emoji‑prefixed commit message.
    """
    _, emoji = _find_keyword(message)
    return f"{emoji} {message}"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.annotate \"<commit message>\"")
        sys.exit(1)
    msg = sys.argv[1]
    print(annotate(msg))


if __name__ == "__main__":
    main()
