"""
Mood Emoji Generator

Maps input text to a mood emoji based on simple keyword heuristics.
"""

from __future__ import annotations
import sys
import re
from typing import List

POSITIVE_WORDS = {"happy", "joy", "love", "awesome", "great", "fantastic", "good", "wonderful", "excited", "pleased"}
NEGATIVE_WORDS = {"sad", "angry", "hate", "bad", "terrible", "awful", "depressed", "upset", "unhappy", "miserable"}


def _tokenize(text: str) -> List[str]:
    """Simple word tokenizer, lower‑cased.
    """
    return re.findall(r"\b\w+\b", text.lower())


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    - Positive sentiment → 😄
    - Negative sentiment → 😞
    - Neutral/unknown   → 😐
    """
    tokens = _tokenize(text)
    pos = sum(tok in POSITIVE_WORDS for tok in tokens)
    neg = sum(tok in NEGATIVE_WORDS for tok in tokens)

    if pos > neg:
        return "😄"
    if neg > pos:
        return "😞"
    return "😐"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m mood_emoji \"Your text here\"")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    print(get_mood_emoji(text))


if __name__ == "__main__":
    main()
