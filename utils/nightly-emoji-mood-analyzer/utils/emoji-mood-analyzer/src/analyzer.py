#!/usr/bin/env python3
"""emoji_mood_analyzer: map free‑form text to a mood emoji.

The implementation is deliberately lightweight – only the Python standard library is used.
"""

from __future__ import annotations
import re
import sys
from typing import List

# Simple keyword sets – feel free to extend!
POSITIVE = {"happy", "joy", "love", "great", "awesome", "fantastic", "good", "wonderful"}
NEGATIVE = {"sad", "angry", "hate", "bad", "terrible", "awful", "depressed", "upset"}


def analyze_mood(text: str) -> str:
    """Return a mood emoji based on keyword matching.

    Rules:
    * Positive words only → 😄
    * Negative words only → 😞
    * Both positive and negative → 😕
    * Neither → 🤔
    """
    # Normalise and extract word tokens
    words = set(re.findall(r"\b\w+\b", text.lower()))
    has_pos = bool(words & POSITIVE)
    has_neg = bool(words & NEGATIVE)

    if has_pos and not has_neg:
        return "😄"
    if has_neg and not has_pos:
        return "😞"
    if has_pos and has_neg:
        return "😕"
    return "🤔"


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: analyzer.py <text>")
        return 2
    text = " ".join(argv)
    print(analyze_mood(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
