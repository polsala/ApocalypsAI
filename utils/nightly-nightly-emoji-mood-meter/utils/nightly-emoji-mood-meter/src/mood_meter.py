"""mood_meter.py

A tiny utility that maps a short piece of text to an emoji representing its overall mood.

The implementation is deliberately lightweight and offline – it relies only on a static keyword‑to‑emoji map.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List

# Simple keyword → emoji mapping. Order matters for overlapping keywords.
_MOOD_MAP: List[tuple[list[str], str]] = [
    (['happy', 'joy', 'love', 'excited', 'glad', 'awesome', 'great'], '😊'),
    (['sad', 'sorrow', 'grief', 'down', 'unhappy', 'depressed'], '😢'),
    (['angry', 'mad', 'furious', 'irate', 'annoyed'], '😠'),
    (['surprised', 'wow', 'shocked', 'amazed'], '😲'),
    (['confused', 'uncertain', 'puzzled', 'meh'], '🤔'),
]

_DEFAULT_EMOJI = '🤔'


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function lower‑cases the input and looks for any of the keywords defined in
    ``_MOOD_MAP``. The first matching group wins. If no keyword is found, ``_DEFAULT_EMOJI``
    is returned.
    """
    lowered = text.lower()
    for keywords, emoji in _MOOD_MAP:
        if any(keyword in lowered for keyword in keywords):
            return emoji
    return _DEFAULT_EMOJI


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert a short text into a mood emoji.')
    parser.add_argument('text', nargs='*', help='Text to analyse (if omitted, reads from stdin)')
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.text:
        input_text = ' '.join(args.text)
    else:
        input_text = sys.stdin.read().strip()
    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == '__main__':
    main()
