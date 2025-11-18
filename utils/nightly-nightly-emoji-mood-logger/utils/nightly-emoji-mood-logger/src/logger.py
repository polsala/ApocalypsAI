"""Emoji Mood Logger utility.

Provides a deterministic, offline function that maps a piece of text to an
emoji representing the overall mood.
"""

from collections import Counter
from typing import Dict, List

# Simple keyword → emoji mapping.
_MOOD_MAP: Dict[str, List[str]] = {
    "happy": ["joy", "glad", "great", "awesome", "fantastic", "good", "well", "smile"],
    "sad": ["sad", "unhappy", "down", "depressed", "bad", "terrible", "sorrow"],
    "angry": ["angry", "mad", "furious", "irritated", "annoyed", "hate"],
    "surprised": ["surprised", "shocked", "wow", "amazed", "astonished"],
    "neutral": [],  # fallback
}

_EMOJI_MAP: Dict[str, str] = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "surprised": "😲",
    "neutral": "😐",
}


def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: split on whitespace and punctuation."""
    import re

    return re.findall(r"\b\w+\b", text.lower())


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The algorithm counts how many keywords from each mood category appear in the
    input and selects the mood with the highest count. Ties are resolved in the
    order defined in ``_MOOD_MAP``. If no keywords match, a neutral emoji is
    returned.
    """
    tokens = _tokenize(text)
    if not tokens:
        return _EMOJI_MAP["neutral"]

    # Count occurrences per mood.
    mood_counts = Counter()
    for mood, keywords in _MOOD_MAP.items():
        for kw in keywords:
            mood_counts[mood] += tokens.count(kw)

    # Determine best mood.
    # Exclude 'neutral' from scoring; it's the fallback.
    best_mood = "neutral"
    best_score = 0
    for mood in _MOOD_MAP.keys():
        if mood == "neutral":
            continue
        score = mood_counts[mood]
        if score > best_score:
            best_score = score
            best_mood = mood

    return _EMOJI_MAP[best_mood]
