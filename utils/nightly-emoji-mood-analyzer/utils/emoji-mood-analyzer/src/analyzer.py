#!/usr/bin/env python3
"""emoji-mood-analyzer

A tiny utility that maps a piece of text to a mood emoji using simple keyword heuristics.

Usage:
    python analyzer.py "I love this!"
    echo "I'm sad" | python analyzer.py
"""

import sys
import argparse
from typing import List, Tuple

# Mapping of mood to (emoji, list of trigger keywords)
MOOD_MAP: List[Tuple[str, List[str]]] = [
    ("😄", ["love", "great", "awesome", "fantastic", "good", "happy", "joy", "excellent", "wonderful"]),
    ("😢", ["sad", "unhappy", "bad", "terrible", "depressed", "down", "sorrow", "cry"]),
    ("😠", ["angry", "mad", "furious", "hate", "annoyed", "irritated", "upset", "rage"]),
    ("😲", ["surprised", "wow", "amazing", "shocked", "astonished", "unexpected"]),
]

NEUTRAL_EMOJI = "😐"


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function lower‑cases the input and checks for the presence of any keyword
    from the MOOD_MAP in order. The first matching mood wins. If no keywords are
    found, the neutral emoji is returned.
    """
    lowered = text.lower()
    for emoji, keywords in MOOD_MAP:
        for kw in keywords:
            if kw in lowered:
                return emoji
    return NEUTRAL_EMOJI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Infer a mood emoji from text.")
    parser.add_argument("text", nargs="?", help="Text to analyze. If omitted, reads from stdin.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.text:
        input_text = args.text
    else:
        # Read from stdin, strip trailing newlines
        input_text = sys.stdin.read().strip()
    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == "__main__":
    main()
