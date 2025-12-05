"""
emoji_generator.py

Provides a function to map mood strings to emojis.
"""

from __future__ import annotations

MOOD_MAP: dict[str, str] = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "tired": "😴",
    "love": "❤️",
    "confused": "🤔",
    "bored": "😐",
    "surprised": "😲",
    "scared": "😱",
}

DEFAULT_EMOJI = "🤔"


def get_emoji(mood: str) -> str:
    """
    Return an emoji representing the given mood.

    Parameters
    ----------
    mood: str
        Mood description (case‑insensitive).

    Returns
    -------
    str
        Corresponding emoji, or a default if unknown.
    """
    if not isinstance(mood, str):
        raise TypeError("mood must be a string")
    return MOOD_MAP.get(mood.strip().lower(), DEFAULT_EMOJI)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Map a mood to an emoji.")
    parser.add_argument("mood", help="Mood description, e.g., happy")
    args = parser.parse_args()
    print(get_emoji(args.mood))


if __name__ == "__main__":
    main()
