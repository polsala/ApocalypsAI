"""emoji_mood_analyzer – simple keyword‑based mood → emoji mapper.

The module provides a single public function ``analyze_mood`` and a tiny CLI
wrapper for convenience.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Tuple

# Mapping of mood to (keyword list, emoji). Order matters for priority.
_MOOD_MAP: List[Tuple[str, List[str], str]] = [
    ("happy", ["happy", "joy", "glad", "awesome", "great", "fantastic"], "😊"),
    ("sad", ["sad", "unhappy", "down", "depressed", "blue"], "😢"),
    ("angry", ["angry", "mad", "furious", "irate", "annoyed"], "😠"),
    ("surprised", ["surprised", "shocked", "amazed", "wow"], "😲"),
]

_DEFAULT_EMOJI = "🤔"


def _normalize(text: str) -> str:
    """Return a lower‑cased version of *text* for case‑insensitive matching."""
    return text.lower()


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function scans the text for the first keyword that appears in the
    ``_MOOD_MAP`` (respecting the defined priority). If no keyword matches, the
    default ``🤔`` emoji is returned.
    """
    lowered = _normalize(text)
    for _mood, keywords, emoji in _MOOD_MAP:
        for kw in keywords:
            if kw in lowered:
                return emoji
    return _DEFAULT_EMOJI


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="emoji-mood-analyzer",
        description="Infer a mood emoji from a short piece of text.",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="The text to analyse. Multiple arguments are joined with spaces.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)
    text = " ".join(args.text)
    emoji = analyze_mood(text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
