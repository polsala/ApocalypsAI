#!/usr/bin/env python3
"""emoji_lookup utility.

Provides:
- `get_emoji(keyword: str) -> str`
- `main()` CLI entry point
"""

from __future__ import annotations
import sys

# Mock rationale: static mapping ensures offline deterministic behaviour.
_EMOJI_MAP = {
    "fire": "🔥",
    "thumbs up": "👍",
    "rocket": "🚀",
    "party": "🥳",
    "coffee": "☕",
    "heart": "❤️",
    "star": "⭐",
    "check": "✅",
    "cross": "❌",
    "question": "❓",
}


def get_emoji(keyword: str) -> str:
    """Return the emoji matching *keyword* (case‑insensitive).

    If the keyword is not found, returns the generic question‑mark emoji.
    """
    key = keyword.strip().lower()
    return _EMOJI_MAP.get(key, _EMOJI_MAP["question"])


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Prints the emoji for the provided keyword or a usage hint.
    Returns:
    - ``0`` on success
    - ``2`` if no keyword was supplied
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m emoji_lookup <keyword>")
        return 2
    keyword = " ".join(argv)
    print(get_emoji(keyword))
    return 0


if __name__ == "__main__":
    sys.exit(main())
