"""emoji_mood_analyzer
=====================

Provides a single public function ``analyze(text: str) -> str`` that returns a mood label based on the emojis present in *text*.

The implementation is deliberately simple and deterministic – it does **not** perform any external network calls or heavy NLP.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

# Mapping of emojis to mood categories. The list is intentionally short for clarity.
_EMOJI_MOOD_MAP: Dict[str, str] = {
    # Happy / Excited
    "😀": "happy",
    "😃": "happy",
    "😄": "happy",
    "😁": "happy",
    "😂": "happy",
    "🤣": "happy",
    "🥳": "happy",
    "🚀": "happy",
    # Sad / Disappointed
    "😢": "sad",
    "😭": "sad",
    "😞": "sad",
    "😔": "sad",
    "☹️": "sad",
    # Angry / Frustrated
    "😠": "angry",
    "😡": "angry",
    "🤬": "angry",
    # Love / Affection
    "❤️": "love",
    "😍": "love",
    "🥰": "love",
    "💖": "love",
    # Neutral / No strong sentiment
    "🤔": "neutral",
    "🤷": "neutral",
    "🙃": "neutral",
}

# Helper list of all known emojis for quick lookup.
_KNOWN_EMOJIS: List[str] = list(_EMOJI_MOOD_MAP.keys())


def _extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in *text* that are present in the mapping.

    The function iterates over each character (or surrogate pair) in the string and
    collects those that match our known set. This is sufficient for the limited
    emoji subset we support.
    """
    emojis: List[str] = []
    i = 0
    while i < len(text):
        char = text[i]
        # Some emojis are represented by two Unicode code points (e.g., "☹️").
        # We attempt to capture a possible variation selector (U+FE0F) by peeking ahead.
        if i + 1 < len(text) and ord(text[i + 1]) == 0xFE0F:
            candidate = char + text[i + 1]
            i += 1  # skip the variation selector
        else:
            candidate = char
        if candidate in _KNOWN_EMOJIS:
            emojis.append(candidate)
        i += 1
    return emojis


def analyze(text: str) -> str:
    """Analyze *text* and return a mood label.

    The algorithm:
    1. Extract known emojis.
    2. Count occurrences per mood.
    3. Return the mood with the highest count.
    4. If no emojis are found, return ``"neutral"``.
    5. In case of a tie, the precedence order is ``happy > love > sad > angry > neutral``.
    """
    emojis = _extract_emojis(text)
    if not emojis:
        return "neutral"

    mood_counter: Counter = Counter()
    for e in emojis:
        mood = _EMOJI_MOOD_MAP.get(e, "neutral")
        mood_counter[mood] += 1

    # Determine the mood with the highest count.
    most_common = mood_counter.most_common()
    if not most_common:
        return "neutral"

    top_count = most_common[0][1]
    tied_moods = [m for m, cnt in most_common if cnt == top_count]

    # Precedence order to break ties deterministically.
    precedence = ["happy", "love", "sad", "angry", "neutral"]
    for pref in precedence:
        if pref in tied_moods:
            return pref
    return "neutral"


def main() -> None:
    """Simple CLI entry point.

    Usage: ``python -m emoji_mood_analyzer "Your text here"``
    """
    import argparse
    parser = argparse.ArgumentParser(description="Infer mood from emojis in a string.")
    parser.add_argument("text", help="Text to analyze")
    args = parser.parse_args()
    mood = analyze(args.text)
    print(mood)


if __name__ == "__main__":
    main()
