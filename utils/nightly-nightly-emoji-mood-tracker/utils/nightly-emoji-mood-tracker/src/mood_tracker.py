"""emoji_mood_tracker
=====================

Provides a function ``mood_to_emoji`` that converts a textual mood into a Unicode emoji.
The module also offers a tiny CLI for quick look‑ups.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Mapping table – feel free to extend!
# ---------------------------------------------------------------------------
MOOD_EMOJI_MAP: Dict[str, str] = {
    "happy": "😄",
    "joy": "🥳",
    "excited": "🤩",
    "sad": "😢",
    "angry": "😠",
    "frustrated": "😤",
    "confused": "🤔",
    "tired": "😴",
    "love": "❤️",
    "surprised": "😲",
    "neutral": "😐",
    "bored": "😐",
    "celebrate": "🎉",
    "party": "🥳",
    "thinking": "🤔",
}


def normalize_mood(mood: str) -> str:
    """Normalize user input for lookup.

    - Strips surrounding whitespace.
    - Lower‑cases the string.
    - Replaces spaces with underscores (e.g., "feeling happy" → "feeling_happy").
    """
    return mood.strip().lower().replace(" ", "_")


def mood_to_emoji(mood: str) -> str:
    """Return the emoji that best matches *mood*.

    If the exact mood is not found, the function attempts a fuzzy fallback by
    checking if any known key is a substring of the normalized mood. If still
    unresolved, a generic "🤷" (shrug) emoji is returned.
    """
    norm = normalize_mood(mood)
    if norm in MOOD_EMOJI_MAP:
        return MOOD_EMOJI_MAP[norm]
    # Fallback: substring match
    for key, emoji in MOOD_EMOJI_MAP.items():
        if key in norm:
            return emoji
    return "🤷"


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Translate a textual mood into a single emoji."
    )
    parser.add_argument(
        "mood",
        type=str,
        help="Mood description (e.g., 'happy', 'frustrated').",
    )
    args = parser.parse_args()
    emoji = mood_to_emoji(args.mood)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module: ``python -m src.mood_tracker <mood>``
    _cli()
