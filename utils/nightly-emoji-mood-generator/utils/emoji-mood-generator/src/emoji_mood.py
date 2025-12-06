"""
emoji_mood.py

Utility to map a textual mood to a list of emojis.
"""

from __future__ import annotations
import argparse
import sys
from typing import List

# Predefined mapping of moods to emojis.
_MOOD_EMOJI_MAP: dict[str, List[str]] = {
    "happy": ["😄", "😊", "🥳"],
    "sad": ["😢", "😞", "☔"],
    "angry": ["😠", "🤬", "🔥"],
    "love": ["❤️", "😍", "💖"],
    "surprised": ["😲", "🤯", "😮"],
    "tired": ["😴", "🥱", "😪"],
    "confused": ["🤔", "😕", "🙃"],
    "celebrate": ["🎉", "🥂", "🍾"],
}


def get_emojis(mood: str) -> List[str]:
    """Return a list of emojis representing the given mood.

    Parameters
    ----------
    mood: str
        Mood description (case‑insensitive). If the mood is not known,
        an empty list is returned.

    Returns
    -------
    List[str]
        List of emoji strings.
    """
    key = mood.strip().lower()
    # Return a copy to prevent accidental mutation of the internal map.
    return _MOOD_EMOJI_MAP.get(key, []).copy()


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map a mood to emojis.")
    parser.add_argument(
        "mood",
        help="Mood word (e.g., happy, sad, love).",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Print the result as a JSON array.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    emojis = get_emojis(args.mood)
    if args.json:
        import json
        print(json.dumps(emojis, ensure_ascii=False))
    else:
        # Join with spaces for readability; print empty string for unknown moods.
        print(" ".join(emojis) if emojis else "")


if __name__ == "__main__":
    main()
