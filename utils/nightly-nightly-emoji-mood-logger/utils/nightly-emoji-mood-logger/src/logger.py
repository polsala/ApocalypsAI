"""emoji_mood_logger
=====================

A tiny sentiment‑to‑emoji mapper.

The public API consists of a single function:

```python
get_mood_emoji(text: str) -> str
```

It returns one of three emojis based on simple keyword matching.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import List

# ---------------------------------------------------------------------------
# Keyword dictionaries – feel free to extend them.
# ---------------------------------------------------------------------------
_POSITIVE_WORDS: List[str] = [
    "happy",
    "joy",
    "great",
    "awesome",
    "fantastic",
    "good",
    "love",
    "excellent",
    "wonderful",
    "pleased",
]

_NEGATIVE_WORDS: List[str] = [
    "sad",
    "bad",
    "terrible",
    "hate",
    "awful",
    "depressed",
    "unhappy",
    "angry",
    "pain",
    "sucks",
]

_EMOJI_MAP = {
    "positive": "😊",
    "negative": "😢",
    "neutral": "😐",
}


def _tokenize(text: str) -> List[str]:
    """Very naive tokenization – split on whitespace and strip punctuation."""
    import string

    translator = str.maketrans("", "", string.punctuation)
    return [word.lower().translate(translator) for word in text.split()]


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The algorithm counts occurrences of known positive and negative keywords.
    If positives outnumber negatives → 😊, if negatives outnumber positives → 😢,
    otherwise → 😐.
    """
    tokens = _tokenize(text)
    counts = Counter(tokens)

    pos_score = sum(counts[word] for word in _POSITIVE_WORDS)
    neg_score = sum(counts[word] for word in _NEGATIVE_WORDS)

    if pos_score > neg_score:
        return _EMOJI_MAP["positive"]
    if neg_score > pos_score:
        return _EMOJI_MAP["negative"]
    return _EMOJI_MAP["neutral"]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Infer mood from a short text and output a corresponding emoji."
    )
    parser.add_argument("text", nargs="+", help="Text to analyse (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module: python -m src.logger "some text"
    _cli()
