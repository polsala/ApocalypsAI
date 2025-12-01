"""emoji_committer
===================

A tiny helper that adds an emoji prefix to a Git commit message based on
keyword detection.

Public API
----------

* ``enhance_message(message: str) -> str`` – Return the message with an
  appropriate emoji, or the original message if no keyword matches.
* ``main()`` – Simple CLI entry point used by the README examples.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Tuple

# Mapping of lower‑case keyword to emoji. Order matters – first match wins.
_KEYWORD_EMOJI_MAP: List[Tuple[str, str]] = [
    ("fix", "🐛"),
    ("bug", "🐛"),
    ("feat", "✨"),
    ("feature", "✨"),
    ("docs", "📝"),
    ("doc", "📝"),
    ("test", "✅"),
    ("tests", "✅"),
    ("refactor", "🔧"),
    ("perf", "⚡"),
    ("performance", "⚡"),
    ("chore", "🔨"),
    ("style", "🎨"),
    ("ci", "🤖"),
]

def _find_emoji(message: str) -> str | None:
    """Return the first matching emoji for *message* or ``None``.

    The search is case‑insensitive and looks for whole‑word occurrences.
    """
    lowered = message.lower()
    for keyword, emoji in _KEYWORD_EMOJI_MAP:
        if keyword in lowered:
            return emoji
    return None


def enhance_message(message: str) -> str:
    """Prepend an emoji to *message* if a known keyword is present.

    Parameters
    ----------
    message:
        The original commit message.

    Returns
    -------
    str
        ``"{emoji} {message}"`` when a keyword matches, otherwise the original
        *message* unchanged.
    """
    emoji = _find_emoji(message)
    if emoji:
        return f"{emoji} {message}"
    return message


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emoji-commit-enhancer",
        description="Add an emoji prefix to a Git commit message based on keywords.",
    )
    parser.add_argument(
        "message",
        help="The commit message to enhance.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    enhanced = enhance_message(args.message)
    print(enhanced)


if __name__ == "__main__":
    # When executed as a script ``python -m emoji_committer "msg"``
    main()
