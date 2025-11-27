"""zen_quote.py

Utility that returns a random Zen‑style quote.

The module provides:
- ``QUOTES`` – a list of dictionaries with ``text``, ``author`` and optional ``tags``.
- ``get_random_quote(tag: str | None = None)`` – returns a random quote matching the tag.
- ``main()`` – CLI entry point.
"""

from __future__ import annotations

import argparse
import random
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# Data – a small curated collection of Zen‑style sayings.
# ---------------------------------------------------------------------------
QUOTES: List[Dict[str, object]] = [
    {
        "text": "The obstacle is the path.",
        "author": "Zen Proverb",
        "tags": ["mindfulness", "obstacle"]
    },
    {
        "text": "When you realize nothing is lacking, the whole world belongs to you.",
        "author": "Zen Proverb",
        "tags": ["gratitude"]
    },
    {
        "text": "If you understand, things are just as they are; if you do not understand, things are just as they are.",
        "author": "Zen Proverb",
        "tags": ["humor"]
    },
    {
        "text": "A jug fills drop by drop.",
        "author": "Zen Proverb",
        "tags": ["patience"]
    },
    {
        "text": "The quieter you become, the more you can hear.",
        "author": "Zen Proverb",
        "tags": ["mindfulness"]
    },
    {
        "text": "When the mind is still, the universe surrenders.",
        "author": "Zen Proverb",
        "tags": ["mindfulness", "spiritual"]
    },
    {
        "text": "A flower does not think of competing with the flower next to it. It just blooms.",
        "author": "Zen Proverb",
        "tags": ["humor", "growth"]
    },
    {
        "text": "The journey of a thousand miles begins with a single step.",
        "author": "Lao Tzu",
        "tags": ["motivation"]
    },
    {
        "text": "When you drink the water, remember the source.",
        "author": "Zen Proverb",
        "tags": ["gratitude"]
    },
    {
        "text": "If you want to know the road ahead, ask those who have traveled it.",
        "author": "Zen Proverb",
        "tags": ["wisdom"]
    },
    {
        "text": "The moon does not care if the night is dark.",
        "author": "Zen Proverb",
        "tags": ["humor"]
    },
    {
        "text": "Silence is a source of great strength.",
        "author": "Zen Proverb",
        "tags": ["mindfulness", "strength"]
    },
]


def _filter_by_tag(quotes: List[Dict[str, object]], tag: str) -> List[Dict[str, object]]:
    """Return only quotes that contain *tag* in their ``tags`` list (case‑insensitive)."""
    tag_lower = tag.lower()
    return [q for q in quotes if any(t.lower() == tag_lower for t in q.get("tags", []))]


def get_random_quote(tag: Optional[str] = None) -> Dict[str, object]:
    """Return a random quote.

    Parameters
    ----------
    tag: str | None
        If provided, only quotes containing this tag are considered.
        If the tag does not match any quote, a ``ValueError`` is raised.
    """
    candidates = QUOTES
    if tag:
        candidates = _filter_by_tag(QUOTES, tag)
        if not candidates:
            raise ValueError(f"No quotes found for tag '{tag}'.")
    # ``random.choice`` is deterministic when a seed is set – callers/tests can patch it.
    return random.choice(candidates)


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., 'humor', 'mindfulness')."
    )
    return parser


def main() -> None:
    args = _build_cli().parse_args()
    try:
        quote = get_random_quote(tag=args.tag)
        print(f"\"{quote['text']}\" — {quote['author']}")
    except ValueError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
