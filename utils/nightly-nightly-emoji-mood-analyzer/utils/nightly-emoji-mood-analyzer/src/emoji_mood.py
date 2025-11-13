#!/usr/bin/env python3
"""
emoji_mood.py

Utility to infer the predominant mood of a text based on emoji usage.
"""

import argparse
import sys
import re
from collections import Counter
from typing import Dict, List

# Mapping of emojis to mood categories
EMOJI_MOOD_MAP: Dict[str, str] = {
    # Happy
    "😀": "happy",
    "😃": "happy",
    "😄": "happy",
    "😁": "happy",
    "😂": "happy",
    "🤣": "happy",
    "😊": "happy",
    "😇": "happy",
    "🙂": "happy",
    "🙃": "happy",
    # Sad
    "☹️": "sad",
    "🙁": "sad",
    "😞": "sad",
    "😔": "sad",
    "😟": "sad",
    "😢": "sad",
    "😭": "sad",
    "😿": "sad",
    # Angry
    "😠": "angry",
    "😡": "angry",
    "🤬": "angry",
    # Love
    "❤️": "love",
    "💖": "love",
    "💘": "love",
    "💕": "love",
    "💝": "love",
    # Surprise
    "😲": "surprise",
    "😮": "surprise",
    "🤯": "surprise",
}

# Pre‑compiled regex to find any of the emojis in the map
EMOJI_PATTERN = re.compile("|".join(map(re.escape, EMOJI_MOOD_MAP.keys())))


def extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in the text that are in EMOJI_MOOD_MAP."""
    return EMOJI_PATTERN.findall(text)


def infer_mood(emojis: List[str]) -> str:
    """Given a list of emojis, return the mood with the highest frequency.

    Ties are resolved alphabetically to keep the result deterministic.
    """
    if not emojis:
        return "neutral"
    mood_counts = Counter(EMOJI_MOOD_MAP[e] for e in emojis)
    most_common = mood_counts.most_common()
    max_count = most_common[0][1]
    top_moods = [m for m, cnt in most_common if cnt == max_count]
    return sorted(top_moods)[0]


def analyze_text(text: str) -> str:
    """Convenient wrapper: extract emojis from text and infer mood."""
    emojis = extract_emojis(text)
    return infer_mood(emojis)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Infer mood from emojis in a piece of text.")
    parser.add_argument(
        "--text",
        required=True,
        help="The text to analyze."
    )
    args = parser.parse_args(argv)
    mood = analyze_text(args.text)
    print(mood)
    return 0

if __name__ == "__main__":
    sys.exit(main())
