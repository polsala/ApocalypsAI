"""emoji_analyzer.py

Utility to infer a simple mood from emojis present in a text.

Supported moods:
- happy
- sad
- angry
- neutral (default / tie)
"""

from collections import Counter
from typing import Dict, List

# Mapping of emojis to mood categories
_EMOJI_MOOD_MAP: Dict[str, str] = {
    # Happy emojis
    "😊": "happy",
    "😄": "happy",
    "😁": "happy",
    "😂": "happy",
    "😃": "happy",
    "😆": "happy",
    # Sad emojis
    "😢": "sad",
    "😞": "sad",
    "😔": "sad",
    "😭": "sad",
    "😿": "sad",
    # Angry emojis
    "😠": "angry",
    "😡": "angry",
    "🤬": "angry",
}

def _extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in *text* that we recognise.

    This function simply iterates over each character; for the purpose of this
    utility we only care about the emojis defined in ``_EMOJI_MOOD_MAP``.
    """
    return [ch for ch in text if ch in _EMOJI_MOOD_MAP]

def analyze_mood(text: str) -> str:
    """Analyze *text* and return the dominant mood.

    Parameters
    ----------
    text: str
        Input string possibly containing emojis.

    Returns
    -------
    str
        One of ``"happy"``, ``"sad"``, ``"angry"`` or ``"neutral"``.
    """
    emojis = _extract_emojis(text)
    if not emojis:
        return "neutral"

    # Count moods
    mood_counts = Counter(_EMOJI_MOOD_MAP[e] for e in emojis)
    # Determine the highest count
    most_common = mood_counts.most_common()
    if len(most_common) == 1:
        return most_common[0][0]
    # If tie for top count, fallback to neutral
    top_count = most_common[0][1]
    tied = [mood for mood, cnt in most_common if cnt == top_count]
    if len(tied) == 1:
        return tied[0]
    return "neutral"

# Simple CLI for manual testing
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Detect mood from emojis in a string.")
    parser.add_argument("text", nargs="?", default="", help="Text to analyze")
    args = parser.parse_args()
    result = analyze_mood(args.text)
    print(result)
    sys.exit(0)
