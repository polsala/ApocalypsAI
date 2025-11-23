"""emoji_mood_analyzer.py

A lightweight sentiment‑to‑emoji mapper.

The algorithm is deliberately simple: it counts occurrences of words from three static lists
(positive, negative, neutral) and picks the emoji with the highest count. In case of a tie, the
neutral emoji is returned.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Word lists – curated for the demo; in a real project these could be expanded.
# ---------------------------------------------------------------------------
POSITIVE_WORDS: List[str] = [
    "love",
    "great",
    "awesome",
    "fantastic",
    "good",
    "happy",
    "excellent",
    "wonderful",
    "amazing",
    "joy",
]

NEGATIVE_WORDS: List[str] = [
    "hate",
    "bad",
    "terrible",
    "awful",
    "sad",
    "angry",
    "worst",
    "pain",
    "disappoint",
    "fail",
]

NEUTRAL_WORDS: List[str] = [
    "the",
    "is",
    "and",
    "it",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
]

EMOJI_MAP = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
}

def _tokenize(text: str) -> List[str]:
    """Very naive tokenization – split on whitespace and strip punctuation."""
    import string

    translator = str.maketrans("", "", string.punctuation)
    return [word.lower().translate(translator) for word in text.split()]

def analyze_mood(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The function counts how many words from each sentiment list appear in the input.
    The category with the highest count wins. Ties fall back to *neutral*.
    """
    tokens = _tokenize(text)
    counts = Counter()
    for token in tokens:
        if token in POSITIVE_WORDS:
            counts["positive"] += 1
        elif token in NEGATIVE_WORDS:
            counts["negative"] += 1
        elif token in NEUTRAL_WORDS:
            counts["neutral"] += 1
        else:
            # Unknown words are ignored – they don't sway the sentiment.
            pass

    # Determine the winning sentiment.
    if not counts:
        # No recognizable words – default to neutral.
        return EMOJI_MAP["neutral"]

    # Find the sentiment(s) with the maximum count.
    max_count = max(counts.values())
    winners = [sent for sent, cnt in counts.items() if cnt == max_count]

    # Tie‑break rule: neutral > positive > negative.
    if "neutral" in winners:
        return EMOJI_MAP["neutral"]
    if "positive" in winners:
        return EMOJI_MAP["positive"]
    return EMOJI_MAP["negative"]

def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Return an emoji representing the sentiment of the supplied text."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="The text to analyze. If omitted, reads from STDIN.",
    )
    return parser

def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)

    if args.text is not None:
        input_text = args.text
    else:
        # Read from stdin when no positional argument is given.
        input_text = sys.stdin.read().strip()

    emoji = analyze_mood(input_text)
    print(emoji)
    return 0

if __name__ == "__main__":
    sys.exit(main())
