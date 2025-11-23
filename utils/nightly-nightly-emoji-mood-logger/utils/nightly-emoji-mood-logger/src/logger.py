"""Emoji Mood Logger utility.

Provides a simple function `get_mood_emoji` that returns an emoji
representing the overall sentiment of a short text string.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List

# Define keyword groups
_HAPPY_KEYWORDS: List[str] = [
    "happy", "joy", "great", "awesome", "fantastic", "good", "excellent",
    "love", "pleased", "delighted", "glad", "wonderful", "amazing"
]
_SAD_KEYWORDS: List[str] = [
    "sad", "bad", "terrible", "unhappy", "depressed", "angry", "frustrated",
    "disappointed", "hate", "upset", "miserable", "sorrow"
]

_HAPPY_EMOJI = "😊"
_SAD_EMOJI = "😢"
_NEUTRAL_EMOJI = "😐"


def _tokenize(text: str) -> List[str]:
    """Return a list of lowercase word tokens from the input.

    Simple word extraction, ignoring punctuation.
    """
    return re.findall(r"\b\w+\b", text.lower())


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The algorithm counts occurrences of happy and sad keywords.
    If happy count > sad count → happy emoji.
    If sad count > happy count → sad emoji.
    Otherwise → neutral emoji.
    """
    tokens = _tokenize(text)
    counter = Counter(tokens)

    happy_score = sum(counter.get(word, 0) for word in _HAPPY_KEYWORDS)
    sad_score = sum(counter.get(word, 0) for word in _SAD_KEYWORDS)

    if happy_score > sad_score:
        return _HAPPY_EMOJI
    if sad_score > happy_score:
        return _SAD_EMOJI
    return _NEUTRAL_EMOJI
