"""emoji_annotator – add emojis to plain‑text strings.

The implementation is deliberately simple: a static mapping from lower‑case words to emojis.
It operates token‑wise, preserving original whitespace and punctuation.
"""

from __future__ import annotations

import re
from typing import Dict

# Static keyword → emoji map. Extend as you wish.
EMOJI_MAP: Dict[str, str] = {
    "love": "❤️",
    "coffee": "☕",
    "cat": "🐱",
    "cats": "🐱",
    "dog": "🐶",
    "doge": "🐕",
    "fire": "🔥",
    "star": "⭐",
    "sun": "☀️",
    "moon": "🌙",
    "music": "🎵",
    "code": "💻",
    "python": "🐍",
    "party": "🥳",
    "cake": "🎂",
    "beer": "🍺",
    "wine": "🍷",
    "book": "📚",
    "rain": "🌧️",
    "snow": "❄️",
}

_word_regex = re.compile(r"(\w+)")


def annotate(text: str) -> str:
    """Return *text* with emojis appended to known words.

    The function is case‑insensitive for matching but preserves the original
    casing in the output. If a word appears in ``EMOJI_MAP`` (lower‑cased), the
    corresponding emoji is appended after a single space.
    """

    def replace(match: re.Match) -> str:
        word = match.group(0)
        emoji = EMOJI_MAP.get(word.lower())
        return f"{word} {emoji}" if emoji else word

    return _word_regex.sub(replace, text)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(annotate(" ".join(sys.argv[1:])))
    else:
        print("Usage: python -m emoji_annotator <text>")
