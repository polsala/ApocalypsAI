#!/usr/bin/env python3
"""
nightly-emoji-annotator

Provides a simple function to annotate sentences with emojis based on keyword detection.
"""

import re
import sys
from typing import List

# Ordered list of (keyword, emoji) pairs – first match wins.
EMOJI_MAP = [
    ("love", "❤️"),
    ("happy", "😊"),
    ("sad", "😢"),
    ("fire", "🔥"),
    ("angry", "😠"),
    ("party", "🥳"),
]


def _pick_emoji(sentence: str) -> str:
    """Return the first matching emoji for the sentence, or empty string."""
    lowered = sentence.lower()
    for keyword, emoji in EMOJI_MAP:
        if keyword in lowered:
            return emoji
    return ""


def annotate(text: str) -> str:
    """
    Annotate each sentence in *text* with an emoji if a keyword is found.

    Sentences are split on punctuation followed by whitespace (., !, ?).
    The original whitespace and punctuation are preserved.
    """
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    annotated_parts: List[str] = []
    for part in parts:
        emoji = _pick_emoji(part)
        if emoji:
            if part[-1] in ".!?":
                annotated = part[:-1] + f" {emoji}" + part[-1]
            else:
                annotated = part + f" {emoji}"
        else:
            annotated = part
        annotated_parts.append(annotated)
    return " ".join(annotated_parts)


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m nightly-emoji-annotator src/annotator.py \"<text>\"")
        sys.exit(1)
    input_text = sys.argv[1]
    print(annotate(input_text))

if __name__ == "__main__":
    _cli()
