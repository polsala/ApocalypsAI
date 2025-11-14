#!/usr/bin/env python3
"""Emoji Mood Analyzer utility.

Provides a simple function `analyze_mood(text: str) -> str` that returns an emoji
representing the sentiment of the supplied text.
"""

import argparse
from typing import List

# Small curated word lists – feel free to extend!
POSITIVE_WORDS: List[str] = [
    "love",
    "happy",
    "joy",
    "wonderful",
    "great",
    "excellent",
    "good",
    "awesome",
    "fantastic",
    "sunny",
    "delight",
    "pleased",
]

NEGATIVE_WORDS: List[str] = [
    "hate",
    "sad",
    "bad",
    "terrible",
    "awful",
    "worst",
    "angry",
    "pain",
    "rain",
    "storm",
    "disappointed",
    "unhappy",
]


def _normalize(word: str) -> str:
    """Lower‑case and strip common punctuation from a token."""
    return word.strip(".,!?:;\"'`).lower()


def score_text(text: str) -> int:
    """Return a simple sentiment score.

    Positive words add +1, negative words subtract -1.
    """
    tokens = [_normalize(tok) for tok in text.split()]
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    return pos - neg


def analyze_mood(text: str) -> str:
    """Map the sentiment score to an emoji.

    - Positive score → 😊
    - Negative score → 😞
    - Zero score → 😐
    """
    score = score_text(text)
    if score > 0:
        return "😊"
    elif score < 0:
        return "😞"
    else:
        return "😐"


def main() -> None:
    parser = argparse.ArgumentParser(description="Return a mood emoji for given text.")
    parser.add_argument(
        "text",
        nargs="+",
        help="Text to analyze (provide as one argument or multiple parts).",
    )
    args = parser.parse_args()
    input_text = " ".join(args.text)
    print(analyze_mood(input_text))


if __name__ == "__main__":
    main()
