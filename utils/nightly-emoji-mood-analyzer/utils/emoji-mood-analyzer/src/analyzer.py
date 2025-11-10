#!/usr/bin/env python3
"""Emoji Mood Analyzer utility.

Analyzes a short piece of text and returns an emoji that best matches the
emotional tone based on simple keyword heuristics.
"""

import argparse
import sys

# Mapping of keywords (lower‑case) to emojis. Order matters – first match wins.
MOOD_MAP = {
    "happy": "😊",
    "joy": "😊",
    "glad": "😊",
    "sad": "😢",
    "unhappy": "😢",
    "down": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
    "love": "❤️",
    "loving": "❤️",
    "affection": "❤️",
}


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function lower‑cases the input and looks for the first keyword present
    in ``MOOD_MAP``. If none are found, a neutral thinking‑face emoji is returned.
    """
    lowered = text.lower()
    for keyword, emoji in MOOD_MAP.items():
        if keyword in lowered:
            return emoji
    return "🤔"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Analyze text mood and output an emoji."
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="Text to analyze (provide as a single argument or multiple words).",
    )
    args = parser.parse_args(argv)
    text = " ".join(args.text)
    emoji = analyze_mood(text)
    print(emoji)


if __name__ == "__main__":
    main()
