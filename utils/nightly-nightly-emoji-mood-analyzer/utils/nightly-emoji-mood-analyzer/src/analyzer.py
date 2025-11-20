"""emoji mood analyzer

Provides a simple function `get_mood_emoji(text: str) -> str` that returns an emoji
representing the overall sentiment of the supplied text. The implementation is
keyword‑based and deliberately lightweight – no external APIs or ML models.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Mapping of mood keywords to emojis. Order matters – first match wins.
MOOD_KEYWORDS: List[Tuple[str, str]] = [
    ("happy|joy|love|thrill|excited|awesome|great|fantastic|wonderful", "😄"),
    ("sad|down|unhappy|depressed|blue|gloom|miserable", "😢"),
    ("angry|mad|furious|irritated|annoyed|hate", "😠"),
    ("surprised|shocked|amazed|wow|unbelievable", "😲"),
    ("fear|scared|terrified|afraid|nervous", "😨"),
]

DEFAULT_EMOJI = "😐"  # neutral


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function lower‑cases the input and searches for the first keyword
    pattern that matches. If none match, a neutral emoji is returned.
    """
    lowered = text.lower()
    for pattern, emoji in MOOD_KEYWORDS:
        # Simple substring check; patterns are pipe‑separated keywords.
        for keyword in pattern.split("|"):
            if keyword in lowered:
                return emoji
    return DEFAULT_EMOJI


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="nightly-emoji-mood-analyzer",
        description="Infer a mood emoji from a piece of text.",
    )
    parser.add_argument("text", nargs="+", help="Text to analyze (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module: `python -m nightly-emoji-mood-analyzer "some text"`
    _cli()
