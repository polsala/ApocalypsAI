"""emoji_mood_analyzer

Provides a single function ``analyze_mood`` that returns a mood label
(``"happy"``, ``"sad"`` or ``"neutral"``) for a given piece of text.

The algorithm is deliberately simple and offline:
1. Count occurrences of a curated set of happy and sad emojis.
2. If emojis give a clear majority, return the corresponding mood.
3. Otherwise, look for a few positive/negative keywords.
4. Default to ``"neutral"``.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List

# ---------------------------------------------------------------------------
# Emoji and keyword definitions
# ---------------------------------------------------------------------------
HAPPY_EMOJIS: List[str] = ["😀", "😃", "😄", "😁", "😊", "😆", "😎", "🤩", "🥳", "👍"]
SAD_EMOJIS: List[str] = ["☹️", "🙁", "😞", "😢", "😔", "😟", "😕", "👎", "💔"]

POSITIVE_KEYWORDS: List[str] = ["love", "great", "awesome", "fantastic", "good", "excellent", "happy", "joy"]
NEGATIVE_KEYWORDS: List[str] = ["hate", "bad", "terrible", "awful", "sad", "pain", "worst", "angry"]

# Pre‑compile regex for performance (offline, deterministic)
EMOJI_PATTERN = re.compile("|".join(map(re.escape, HAPPY_EMOJIS + SAD_EMOJIS)))
POSITIVE_PATTERN = re.compile(r"\\b(?:" + "|".join(POSITIVE_KEYWORDS) + r")\\b", re.IGNORECASE)
NEGATIVE_PATTERN = re.compile(r"\\b(?:" + "|".join(NEGATIVE_KEYWORDS) + r")\\b", re.IGNORECASE)


def _count_emojis(text: str) -> Counter:
    """Return a Counter with counts for happy and sad emojis found in *text*."""
    matches = EMOJI_PATTERN.findall(text)
    counter = Counter()
    for emoji in matches:
        if emoji in HAPPY_EMOJIS:
            counter["happy"] += 1
        elif emoji in SAD_EMOJIS:
            counter["sad"] += 1
    return counter


def _count_keywords(text: str) -> Counter:
    """Return a Counter with counts for positive and negative keywords."""
    counter = Counter()
    counter["happy"] = len(POSITIVE_PATTERN.findall(text))
    counter["sad"] = len(NEGATIVE_PATTERN.findall(text))
    return counter


def analyze_mood(text: str) -> str:
    """Analyze *text* and return ``"happy"``, ``"sad"`` or ``"neutral"``.

    The decision hierarchy is:
    1. Emoji majority → return that mood.
    2. Keyword majority → return that mood.
    3. No clear majority → ``"neutral"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    emoji_counts = _count_emojis(text)
    if emoji_counts["happy"] > emoji_counts["sad"]:
        return "happy"
    if emoji_counts["sad"] > emoji_counts["happy"]:
        return "sad"

    keyword_counts = _count_keywords(text)
    if keyword_counts["happy"] > keyword_counts["sad"]:
        return "happy"
    if keyword_counts["sad"] > keyword_counts["happy"]:
        return "sad"

    return "neutral"
