"""emoji_analyzer.py

A tiny, self‑contained emoji mood analyzer.

The public API consists of a single function:

    analyze_mood(text: str) -> str

which returns one of "happy", "sad" or "neutral".
"""

from __future__ import annotations

import sys
from collections import Counter
from typing import Dict

# ---------------------------------------------------------------------------
# Emoji sentiment map (very small on purpose – offline & deterministic)
# Positive emojis contribute +1, negative emojis –1. All others are ignored.
# ---------------------------------------------------------------------------
EMOJI_MOOD_MAP: Dict[str, int] = {
    "😀": 1,
    "😃": 1,
    "😄": 1,
    "😁": 1,
    "😂": 1,
    "🥳": 1,
    "❤️": 1,
    "😍": 1,
    "👍": 1,
    "🙌": 1,
    "😢": -1,
    "😭": -1,
    "😞": -1,
    "😔": -1,
    "👎": -1,
    "💔": -1,
    "😡": -1,
    "😠": -1,
}


def _extract_emojis(text: str) -> list[str]:
    """Return a list of emojis found in *text* that are present in the mood map.

    This helper isolates the extraction logic so it can be unit‑tested or
    mocked independently.
    """
    return [ch for ch in text if ch in EMOJI_MOOD_MAP]


def analyze_mood(text: str) -> str:
    """Analyze *text* and return a mood classification.

    Parameters
    ----------
    text: str
        Input string possibly containing emojis.

    Returns
    -------
    str
        One of "happy", "sad" or "neutral".
    """
    emojis = _extract_emojis(text)
    if not emojis:
        return "neutral"

    score = sum(EMOJI_MOOD_MAP[e] for e in emojis)
    if score > 0:
        return "happy"
    if score < 0:
        return "sad"
    return "neutral"


def _cli() -> None:
    """Simple command‑line interface.

    Usage: python -m utils.nightly-emoji-mood-analyzer.src.emoji_analyzer "some text"
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-mood-analyzer.src.emoji_analyzer \"<text>\"")
        sys.exit(1)
    text = sys.argv[1]
    print(analyze_mood(text))


if __name__ == "__main__":
    _cli()
