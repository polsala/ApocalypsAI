"""
Daily Zen Quote Generator

Provides a simple API to fetch random Zen quotes.
"""

import random
import sys
from typing import List, Optional

# Built‑in quote database
_QUOTES = [
    {"text": "The journey of a thousand miles begins with one step.", "tags": ["mindfulness"]},
    {"text": "When the mind is still, the universe surrenders.", "tags": ["mindfulness"]},
    {"text": "If you cannot find the truth within yourself, look elsewhere.", "tags": ["humor"]},
    {"text": "A wise man once said nothing at all.", "tags": ["humor"]},
    {"text": "The sound of one hand clapping is a great debugging tool.", "tags": ["humor", "tech"]},
]


def get_quote(tag: Optional[str] = None) -> str:
    """
    Return a random quote. If ``tag`` is provided, only quotes containing that tag are considered.
    Raises ``ValueError`` if no quotes match the tag.
    """
    candidates: List[dict] = _QUOTES
    if tag:
        candidates = [q for q in _QUOTES if tag.lower() in (t.lower() for t in q["tags"])]
        if not candidates:
            raise ValueError(f"No quotes found for tag '{tag}'")
    quote = random.choice(candidates)
    return quote["text"]


def _parse_args(argv: List[str]) -> Optional[str]:
    """Simple CLI parser; returns tag or None."""
    if "--tag" in argv:
        idx = argv.index("--tag")
        try:
            return argv[idx + 1]
        except IndexError:
            raise ValueError("Missing tag value after '--tag'")
    return None


def main() -> None:
    try:
        tag = _parse_args(sys.argv[1:])
        print(get_quote(tag))
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
