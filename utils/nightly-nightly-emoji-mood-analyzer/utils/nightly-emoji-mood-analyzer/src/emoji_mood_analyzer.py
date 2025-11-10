"""emoji_mood_analyzer

A tiny command‑line utility that maps input text to a mood emoji.

Usage:
    python -m src.emoji_mood_analyzer "I am happy"
"""

import argparse
import sys
from typing import Dict, List

# Simple keyword → emoji mapping
MOOD_MAP: Dict[str, str] = {
    "happy": "😊",
    "joy": "😊",
    "glad": "😊",
    "love": "❤️",
    "excited": "🤩",
    "sad": "😢",
    "unhappy": "😢",
    "angry": "😠",
    "mad": "😠",
    "tired": "😴",
    "sleepy": "😴",
    "confused": "🤔",
    "bored": "😐",
    "surprised": "😲",
    "fear": "😨",
    "scared": "😨",
}

def get_mood_emoji(text: str) -> str:
    """Return the first matching mood emoji for *text*.

    The function lower‑cases the input and checks each keyword in
    ``MOOD_MAP``. If none match, it returns a default thinking face.
    """
    lowered = text.lower()
    for keyword, emoji in MOOD_MAP.items():
        if keyword in lowered:
            return emoji
    return "🤔"  # default when no mood detected

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Infer a mood emoji from a line of text."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="The text to analyse. If omitted, reads from stdin.",
    )
    return parser

def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.text is not None:
        input_text = args.text
    else:
        # Read from stdin when no argument supplied
        input_text = sys.stdin.read().strip()

    emoji = get_mood_emoji(input_text)
    print(emoji)
    return 0

if __name__ == "__main__":
    sys.exit(main())
