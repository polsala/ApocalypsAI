"""emoji_mood_analyzer
=====================

A tiny module that maps short English sentences to an emoji representing the overall mood.

The algorithm is deliberately simple and deterministic:

1. Lower‑case the input.
2. Count occurrences of *positive* and *negative* keywords.
3. Return an emoji based on which count is higher (or neutral).

The implementation is self‑contained and has no external dependencies.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import List

_POSITIVE_KEYWORDS: List[str] = [
    "love",
    "happy",
    "joy",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excited",
    "delight",
]

_NEGATIVE_KEYWORDS: List[str] = [
    "sad",
    "hate",
    "angry",
    "bad",
    "terrible",
    "awful",
    "depressed",
    "gloomy",
    "upset",
    "pain",
]

_EMOJI_MAP = {
    "positive": "😄",
    "negative": "😔",
    "neutral": "😐",
}


def _tokenize(text: str) -> List[str]:
    """Very naive tokenization – split on whitespace and strip punctuation."""
    import string

    translator = str.maketrans("", "", string.punctuation)
    return [word.translate(translator).lower() for word in text.split()]


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function counts how many positive and negative keywords appear in the
    input. If positives > negatives → positive emoji, if negatives > positives →
    negative emoji, otherwise neutral.
    """
    tokens = _tokenize(text)
    counts = Counter(tokens)
    pos_score = sum(counts[k] for k in _POSITIVE_KEYWORDS)
    neg_score = sum(counts[k] for k in _NEGATIVE_KEYWORDS)

    if pos_score > neg_score:
        return _EMOJI_MAP["positive"]
    if neg_score > pos_score:
        return _EMOJI_MAP["negative"]
    return _EMOJI_MAP["neutral"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Infer mood of a short text and output an emoji.")
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyze. If omitted, reads from stdin.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)
    if args.text:
        text = args.text
    else:
        # Read from stdin until EOF
        text = sys.stdin.read().strip()
    if not text:
        parser.error("No input text provided.")
        return 1
    emoji = analyze_mood(text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
