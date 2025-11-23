"""logger.py

Simple mood‑to‑emoji mapper.

The logic is intentionally straightforward: we look for the presence of
pre‑defined *happy* or *sad* keywords (case‑insensitive). If any happy keyword
appears, we return the happy emoji. If any sad keyword appears (and no happy
keyword), we return the sad emoji. Otherwise we fall back to a neutral emoji.

This module has **no external dependencies** and can be imported directly.
"""

from __future__ import annotations

import re
from typing import List

# Keyword lists – kept short for clarity; can be extended by users.
_HAPPY_KEYWORDS: List[str] = [
    "happy",
    "joy",
    "love",
    "great",
    "awesome",
    "fantastic",
    "good",
    "excellent",
]

_SAD_KEYWORDS: List[str] = [
    "sad",
    "bad",
    "terrible",
    "hate",
    "upset",
    "fail",
    "failed",
    "error",
    "problem",
]

_HAPPY_EMOJI = "😊"
_SAD_EMOJI = "😢"
_NEUTRAL_EMOJI = "😐"


def _contains_keyword(text: str, keywords: List[str]) -> bool:
    """Return ``True`` if any keyword appears in *text* (case‑insensitive).

    The check uses word boundaries to avoid accidental matches inside other
    words (e.g., ``"sadness"`` still counts as sad, but ``"glad"`` does not).
    """
    pattern = r"\\b(?:" + "|".join(map(re.escape, keywords)) + r")\\b"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    Parameters
    ----------
    text: str
        Input string to analyse.

    Returns
    -------
    str
        One of ``😊``, ``😢`` or ``😐``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Happy takes precedence – a message can be both happy and sad, but we
    # consider the positive sentiment the dominant one for this simple heuristic.
    if _contains_keyword(text, _HAPPY_KEYWORDS):
        return _HAPPY_EMOJI
    if _contains_keyword(text, _SAD_KEYWORDS):
        return _SAD_EMOJI
    return _NEUTRAL_EMOJI


# Simple CLI for manual experimentation (not required for tests).
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m logger \"your text here\"")
        sys.exit(1)
    input_text = " ".join(sys.argv[1:])
    print(get_mood_emoji(input_text))
