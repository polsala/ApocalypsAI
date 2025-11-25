"""emoji_mood_analyzer
~~~~~~~~~~~~~~~~~~~~~~

Provides a simple sentiment‑to‑emoji conversion.

Public API
----------
- ``analyze_mood(text: str) -> str``: Returns one of ``"😊"``, ``"😐"`` or ``"😞"``.
- ``_load_word_lists() -> tuple[set[str], set[str]]``: Internal helper that loads the positive
  and negative word sets. In production it reads from the module‑level constants, but the function
  exists to make mocking trivial in tests.
"""

from __future__ import annotations

import re
from typing import Set, Tuple

# ---------------------------------------------------------------------------
# Default word lists (tiny but illustrative).  Real‑world usage would replace
# these with a more exhaustive list.
# ---------------------------------------------------------------------------
_POSITIVE_WORDS: Set[str] = {
    "good",
    "great",
    "awesome",
    "fantastic",
    "love",
    "excellent",
    "happy",
    "joy",
    "wonderful",
    "nice",
}

_NEGATIVE_WORDS: Set[str] = {
    "bad",
    "terrible",
    "awful",
    "hate",
    "poor",
    "sad",
    "angry",
    "worst",
    "bug",
    "fail",
}


def _load_word_lists() -> Tuple[Set[str], Set[str]]:
    """Return the positive and negative word sets.

    The function is deliberately isolated so that unit tests can monkey‑patch it
    with deterministic mock data without touching the module globals.
    """
    # Mock rationale: In a real utility we might load from a file or external
    # resource. Keeping it simple ensures offline determinism.
    return _POSITIVE_WORDS, _NEGATIVE_WORDS


def _tokenize(text: str) -> list[str]:
    """Split *text* into lowercase word tokens, stripping punctuation.

    Simple regex based tokenizer – sufficient for short sentences.
    """
    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> str:
    """Analyze *text* and return an emoji representing its mood.

    Parameters
    ----------
    text: str
        Input string to evaluate.

    Returns
    -------
    str
        ``"😊"`` if positive > negative,
        ``"😞"`` if negative > positive,
        ``"😐"`` otherwise.
    """
    pos_words, neg_words = _load_word_lists()
    tokens = _tokenize(text)
    pos_count = sum(1 for t in tokens if t in pos_words)
    neg_count = sum(1 for t in tokens if t in neg_words)

    if pos_count > neg_count:
        return "😊"
    if neg_count > pos_count:
        return "😞"
    return "😐"


# ---------------------------------------------------------------------------
# CLI entry‑point – allows ``python -m src.mood_analyzer "some text"``
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Return a mood emoji for a short text.")
    parser.add_argument("text", nargs="+", help="Text to analyze (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    emoji = analyze_mood(input_text)
    sys.stdout.write(emoji + "\n")
