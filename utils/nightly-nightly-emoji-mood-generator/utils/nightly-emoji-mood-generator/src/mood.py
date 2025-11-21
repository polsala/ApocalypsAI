import argparse
import sys
from typing import Dict

# Mapping of mood keywords to emojis. Extend as you like.
MOOD_EMOJI_MAP: Dict[str, str] = {
    "happy": "😊",
    "joy": "😂",
    "excited": "🤩",
    "love": "❤️",
    "sad": "😢",
    "angry": "😠",
    "confused": "🤔",
    "tired": "😴",
    "surprised": "😲",
    "neutral": "😐",
}

DEFAULT_EMOJI = "😐"


def get_emoji(mood: str) -> str:
    """Return the emoji for *mood*.

    The lookup is case‑insensitive and falls back to ``DEFAULT_EMOJI`` when the
    mood is not recognised.
    """
    normalized = mood.strip().lower()
    return MOOD_EMOJI_MAP.get(normalized, DEFAULT_EMOJI)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a textual mood into an emoji."
    )
    parser.add_argument(
        "mood",
        help="Mood description (e.g., 'happy', 'sad', 'confused').",
    )
    args = parser.parse_args(argv)
    emoji = get_emoji(args.mood)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
