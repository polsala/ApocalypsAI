"""daily-zen-quote-dispenser – random Zen quote CLI.

Provides a small collection of quotes and a helper to fetch a random one.
Optionally filter by theme and/or seed the random generator for reproducible
output.
"""

import argparse
import random
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Quote database – each entry has a `text` and a `theme`.
# ---------------------------------------------------------------------------
QUOTES: List[Dict[str, str]] = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "growth"},
    {"text": "When you realize nothing is lacking, the whole world belongs to you.", "theme": "mindfulness"},
    {"text": "Silence is a source of great strength.", "theme": "mindfulness"},
    {"text": "Fall seven times, stand up eight.", "theme": "resilience"},
    {"text": "The obstacle is the path.", "theme": "growth"},
]


def _filter_by_theme(quotes: List[Dict[str, str]], theme: Optional[str]) -> List[Dict[str, str]]:
    """Return only quotes matching *theme* (case‑insensitive)."""
    if not theme:
        return quotes
    theme_lower = theme.lower()
    return [q for q in quotes if q["theme"].lower() == theme_lower]


def get_random_quote(seed: Optional[int] = None, theme: Optional[str] = None) -> Optional[str]:
    """Return a random quote string.

    * ``seed`` – if provided, seeds ``random`` for deterministic output.
    * ``theme`` – optional filter; if no quotes match, ``None`` is returned.
    """
    if seed is not None:
        random.seed(seed)
    filtered = _filter_by_theme(QUOTES, theme)
    if not filtered:
        return None
    choice = random.choice(filtered)
    return choice["text"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument("--theme", type=str, help="Filter quotes by theme (e.g., mindfulness, growth)")
    parser.add_argument("--seed", type=int, help="Seed for deterministic output")
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    quote = get_random_quote(seed=args.seed, theme=args.theme)
    if quote:
        print(quote)
    else:
        print("No quotes found for the specified theme.")


if __name__ == "__main__":
    main()
