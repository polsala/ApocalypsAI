"""emoji_mood_analyzer

A small, self‑contained utility that infers a simple mood from emojis present in a text.

Supported moods:
- ``happy`` – 😊 😄 😁 😃
- ``sad``   – 😢 😞 😔 😿
- ``angry`` – 😡 😠 🤬

If no known emojis are found, or if multiple moods have the same highest score, ``neutral`` is returned.
"""

from __future__ import annotations

import sys
from collections import Counter
from typing import Dict, List

# Mapping of emoji to mood
_EMOJI_MOOD_MAP: Dict[str, str] = {
    "😊": "happy",
    "😄": "happy",
    "😁": "happy",
    "😃": "happy",
    "😢": "sad",
    "😞": "sad",
    "😔": "sad",
    "😿": "sad",
    "😡": "angry",
    "😠": "angry",
    "🤬": "angry",
}

def _extract_emojis(text: str) -> List[str]:
    """Return a list of emojis from *text* that are present in the mapping.

    This is a very lightweight extractor – it simply iterates over characters
    and keeps those that appear in ``_EMOJI_MOOD_MAP``.
    """
    return [ch for ch in text if ch in _EMOJI_MOOD_MAP]

def analyze_mood(text: str) -> str:
    """Analyze *text* and return one of ``"happy"``, ``"sad"``, ``"angry"`` or ``"neutral"``.

    The algorithm counts each known emoji toward its associated mood. The mood
    with the highest count wins. In case of a tie or when no known emojis are
    present, ``"neutral"`` is returned.
    """
    emojis = _extract_emojis(text)
    if not emojis:
        return "neutral"

    mood_counts = Counter(_EMOJI_MOOD_MAP[e] for e in emojis)
    most_common = mood_counts.most_common()
    if len(most_common) == 0:
        return "neutral"
    top_mood, top_score = most_common[0]
    # Check for tie
    if len(most_common) > 1 and most_common[1][1] == top_score:
        return "neutral"
    return top_mood

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-mood-analyzer.src.analyzer \"<text>\"")
        sys.exit(2)
    text = sys.argv[1]
    mood = analyze_mood(text)
    print(mood)

if __name__ == "__main__":
    _cli()
