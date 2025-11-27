"""emoji_mood_analyzer

Provides a single public function ``analyze_mood`` that returns an emoji representing the
sentiment of the supplied text.

The implementation is deliberately lightweight: it scans the text for a handful of
keywords associated with four moods – happy, sad, angry, neutral – and picks the first
matching mood. If no keywords are found, the mood defaults to neutral.
"""

from __future__ import annotations

import argparse
import re
from typing import Dict, List

# Mapping of mood -> (emoji, list of trigger words)
_MOOD_MAP: Dict[str, tuple[str, List[str]]] = {
    "happy": ("😄", ["happy", "joy", "love", "wonderful", "great", "awesome", "fantastic", "good", "glad"]),
    "sad": ("😢", ["sad", "unhappy", "bad", "terrible", "depressed", "down", "cry", "sorrow"]),
    "angry": ("😠", ["angry", "mad", "furious", "irate", "annoyed", "hate", "rage"]),
    "neutral": ("😐", []),
}

# Pre‑compile regex patterns for performance and case‑insensitivity
_MOOD_PATTERNS: List[tuple[str, re.Pattern]] = []
for mood, (_, keywords) in _MOOD_MAP.items():
    if keywords:
        pattern = re.compile(r"\\b(?:" + "|".join(map(re.escape, keywords)) + r")\\b", re.IGNORECASE)
        _MOOD_PATTERNS.append((mood, pattern))


def analyze_mood(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The function checks the text against the keyword lists defined in ``_MOOD_MAP``.
    The first mood whose pattern matches wins. If none match, ``neutral`` is returned.

    Parameters
    ----------
    text: str
        Input text to analyse.

    Returns
    -------
    str
        A single Unicode emoji.
    """
    for mood, pattern in _MOOD_PATTERNS:
        if pattern.search(text):
            return _MOOD_MAP[mood][0]
    # Default to neutral
    return _MOOD_MAP["neutral"][0]


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a short piece of text and output a mood emoji.")
    parser.add_argument("text", type=str, help="The text to analyse")
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    emoji = analyze_mood(args.text)
    print(emoji)


if __name__ == "__main__":
    main()
