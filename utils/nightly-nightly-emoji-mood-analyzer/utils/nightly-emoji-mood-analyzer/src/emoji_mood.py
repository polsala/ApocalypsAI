"""
emoji_mood.py

Provides `analyze_mood` to determine the dominant emoji mood in a text.
"""

from collections import Counter
from typing import Dict, List

# Mapping emojis to mood categories
MOOD_EMOJIS: Dict[str, List[str]] = {
    "happy": ["😀", "😃", "😄", "😁", "😊", "😆", "😎"],
    "sad": ["😢", "😭", "😞", "☹️", "🙁", "😔"],
    "angry": ["😠", "😡", "🤬", "👿"],
    "love": ["❤️", "😍", "😘", "💕", "💖", "💘"],
}

# Inverse map for quick lookup
EMOJI_TO_MOOD: Dict[str, str] = {
    emoji: mood for mood, emojis in MOOD_EMOJIS.items() for emoji in emojis
}

# Priority order for tie‑breaking
MOOD_PRIORITY = ["love", "happy", "sad", "angry"]


def analyze_mood(text: str) -> str:
    """
    Return the dominant mood based on emoji frequency.

    Parameters
    ----------
    text: str
        Input text possibly containing emojis.

    Returns
    -------
    str
        One of the mood keys ("happy", "sad", "angry", "love") or "neutral"
        if no known emojis are found.
    """
    counts = Counter()
    for char in text:
        mood = EMOJI_TO_MOOD.get(char)
        if mood:
            counts[mood] += 1

    if not counts:
        return "neutral"

    max_count = max(counts.values())
    candidates = [m for m, c in counts.items() if c == max_count]
    for mood in MOOD_PRIORITY:
        if mood in candidates:
            return mood
    return candidates[0]  # Fallback, should not happen


def _cli():
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Determine dominant emoji mood.")
    parser.add_argument("path", help="Path to a text file")
    args = parser.parse_args()
    try:
        with open(args.path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    mood = analyze_mood(content)
    print(mood)

if __name__ == "__main__":
    _cli()
