"""emoji_mood_indicator

A tiny helper that maps textual moods to emojis.

Provides:
- `get_mood_emoji(mood: str) -> str`
- CLI entry point via `python -m src.mood <mood>`
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Mapping of normalized mood strings to emojis
MOOD_MAP: Dict[str, str] = {
    "happy": "😊",
    "joy": "😊",
    "joyful": "😊",
    "excited": "🤩",
    "thrilled": "🤩",
    "sad": "😢",
    "down": "😢",
    "depressed": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
    "confused": "🤔",
    "uncertain": "🤔",
    "thinking": "🤔",
    "love": "❤️",
    "loved": "❤️",
    "tired": "😴",
    "sleepy": "😴",
    "bored": "😐",
    "neutral": "😐",
}

DEFAULT_EMOJI = "❓"


def get_mood_emoji(mood: str) -> str:
    """Return the emoji representing *mood*.

    The lookup is case‑insensitive and ignores surrounding whitespace.
    If the mood is not recognised, ``DEFAULT_EMOJI`` is returned.
    """
    normalized = mood.strip().lower()
    return MOOD_MAP.get(normalized, DEFAULT_EMOJI)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a textual mood into an emoji.")
    parser.add_argument("mood", help="Mood description (e.g., happy, sad, angry)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    emoji = get_mood_emoji(args.mood)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
