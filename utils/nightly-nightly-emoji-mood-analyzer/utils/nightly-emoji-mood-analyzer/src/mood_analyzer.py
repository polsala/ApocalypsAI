"""mood_analyzer.py

A tiny sentiment‑to‑emoji mapper.

The algorithm is deliberately simple: it counts occurrences of words from three static sets
(positive, negative, angry). The highest count determines the mood; ties fall back to neutral.

This module provides:
- `analyze_mood(text: str) -> str` – returns an emoji.
- A small CLI for convenience.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import Iterable, Set

# ---------------------------------------------------------------------------
# Word lists – deliberately short for deterministic behaviour.
# ---------------------------------------------------------------------------
POSITIVE_WORDS: Set[str] = {
    "love",
    "happy",
    "joy",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "delight",
    "sunny",
    "smile",
}

NEGATIVE_WORDS: Set[str] = {
    "sad",
    "bad",
    "terrible",
    "horrible",
    "depressed",
    "unhappy",
    "gloomy",
    "miserable",
    "cry",
    "tears",
    "rainy",
}

ANGRY_WORDS: Set[str] = {
    "angry",
    "mad",
    "furious",
    "irate",
    "annoyed",
    "rage",
    "hate",
    "frustrated",
    "outraged",
    "pissed",
}

MOOD_EMOJI = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "🤔",
}

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> Iterable[str]:
    """Very simple tokenizer – split on whitespace and strip punctuation.

    This keeps the utility lightweight and deterministic.
    """
    for raw in text.lower().split():
        # Strip common punctuation characters
        token = raw.strip(".,!?:;\"'()[]{}")
        if token:
            yield token


def _count_matches(tokens: Iterable[str], word_set: Set[str]) -> int:
    """Count how many tokens appear in *word_set*.
    """
    return sum(1 for token in tokens if token in word_set)


def analyze_mood(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The algorithm:
    1. Tokenize the input.
    2. Count matches against the three word lists.
    3. Choose the mood with the highest count.
    4. If all counts are zero or there is a tie, return the neutral emoji.
    """
    tokens = list(_tokenize(text))
    if not tokens:
        return MOOD_EMOJI["neutral"]

    counts = Counter({
        "happy": _count_matches(tokens, POSITIVE_WORDS),
        "sad": _count_matches(tokens, NEGATIVE_WORDS),
        "angry": _count_matches(tokens, ANGRY_WORDS),
    })

    # Determine the mood with the highest count
    most_common = counts.most_common()
    if not most_common:
        return MOOD_EMOJI["neutral"]

    top_mood, top_score = most_common[0]
    # Check for tie with second place
    if len(most_common) > 1 and top_score == most_common[1][1]:
        return MOOD_EMOJI["neutral"]

    # If no words matched, fall back to neutral
    if top_score == 0:
        return MOOD_EMOJI["neutral"]

    return MOOD_EMOJI[top_mood]

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Return an emoji representing the mood of the supplied text."
    )
    parser.add_argument("text", nargs="+", help="Text to analyze (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    emoji = analyze_mood(input_text)
    print(emoji)

if __name__ == "__main__":
    # When executed as a script, act as a tiny CLI.
    _cli()
