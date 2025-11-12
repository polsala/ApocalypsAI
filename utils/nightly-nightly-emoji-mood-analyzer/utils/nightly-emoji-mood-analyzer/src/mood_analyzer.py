"""mood_analyzer.py

A tiny, dependency‑free mood‑to‑emoji mapper.

Provides:
* ``analyze_mood(text: str) -> str`` – core function used by CLI and tests.
* ``main()`` – simple ``argparse`` entry‑point.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import Dict, List

# ---------------------------------------------------------------------------
# Keyword → Emoji mapping (order matters for tie‑breaking)
# ---------------------------------------------------------------------------
_MOOD_MAP: List[tuple[str, List[str], str]] = [
    ("happy", ["happy", "love", "great", "awesome", "fantastic", "wonderful"], "😄"),
    ("sad", ["sad", "disappointed", "bad", "terrible", "upset"], "😢"),
    ("angry", ["angry", "furious", "hate", "mad", "outraged"], "😠"),
    ("surprised", ["surprised", "wow", "amazing", "unbelievable", "shocking"], "😲"),
]

# Fallback emoji when no keywords match
_DEFAULT_EMOJI = "😐"


def _build_lookup() -> Dict[str, str]:
    """Create a token → emoji mapping for fast lookup.

    Returns
    -------
    dict
        Mapping from lower‑cased keyword to its associated emoji.
    """
    lookup: Dict[str, str] = {}
    for _category, keywords, emoji in _MOOD_MAP:
        for kw in keywords:
            lookup[kw] = emoji
    return lookup

_LOOKUP = _build_lookup()


def analyze_mood(text: str) -> str:
    """Return the emoji that best represents the *dominant* mood in ``text``.

    The algorithm is deliberately simple:
    1. Tokenise ``text`` on whitespace.
    2. Lower‑case each token and look it up in the keyword table.
    3. Count hits per emoji.
    4. Choose the emoji with the highest count; ties are resolved by the
       order defined in ``_MOOD_MAP``.
    5. If no keywords are found, return ``_DEFAULT_EMOJI``.

    Parameters
    ----------
    text: str
        Input string to analyse.

    Returns
    -------
    str
        A single emoji character.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    tokens = text.lower().split()
    emoji_counter: Counter[str] = Counter()
    for token in tokens:
        emoji = _LOOKUP.get(token)
        if emoji:
            emoji_counter[emoji] += 1

    if not emoji_counter:
        return _DEFAULT_EMOJI

    # Resolve ties by the predefined order in _MOOD_MAP
    for _category, _keywords, emoji in _MOOD_MAP:
        if emoji_counter.get(emoji):
            # This is the first emoji (in order) that has a non‑zero count
            return emoji
    # Fallback – should never hit because we already checked counter non‑empty
    return _DEFAULT_EMOJI


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emoji-mood-analyzer",
        description="Return a single emoji representing the dominant mood of the supplied text.",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="Text to analyse. Provide as a single quoted string or multiple words.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    # ``args.text`` is a list of words; join them back to a single string
    input_text = " ".join(args.text)
    emoji = analyze_mood(input_text)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module: ``python -m utils.nightly-emoji-mood-analyzer.src.mood_analyzer "..."``
    main()
