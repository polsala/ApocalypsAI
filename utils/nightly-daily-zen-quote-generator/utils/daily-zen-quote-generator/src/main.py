"""Daily Zen Quote Generator.

Provides `get_zen_quote` function and a simple CLI.
"""

import random
import sys
from typing import List, Optional

_QUOTES: List[dict] = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "motivation"},
    {"text": "When the mind is still, the universe surrenders.", "theme": "mindfulness"},
    {"text": "Simplicity is the ultimate sophistication.", "theme": "simplicity"},
    {"text": "Let go of attachment and find freedom.", "theme": "freedom"},
    {"text": "Observe the breath, observe the mind.", "theme": "mindfulness"},
]


def get_zen_quote(theme: Optional[str] = None) -> str:
    """Return a random Zen quote.

    Args:
        theme: Optional theme to filter quotes (case‑insensitive).

    Returns:
        A quote string.

    Raises:
        ValueError: If no quotes match the given theme.
    """
    if theme:
        filtered = [q["text"] for q in _QUOTES if q["theme"].lower() == theme.lower()]
        if not filtered:
            raise ValueError(f"No quotes found for theme '{theme}'.")
        return random.choice(filtered)
    return random.choice([q["text"] for q in _QUOTES])


def _cli() -> None:
    """Simple command‑line interface."""
    theme = None
    if len(sys.argv) > 1:
        theme = sys.argv[1]
    try:
        print(get_zen_quote(theme))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
