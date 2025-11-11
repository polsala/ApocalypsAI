"""daily_motivation_quote

A tiny CLI that prints a random motivational quote.

The module provides:
- `get_random_quote(category: str | None = None, seed: int | None = None) -> str`
- `main()` entry‑point for ``python -m daily_motivation_quote``.

All data lives in‑memory; no network calls are made.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import List, Optional

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Quote:
    text: str
    category: Optional[str] = None

# A small curated list of quotes. Feel free to extend.
_QUOTES: List[Quote] = [
    Quote("The only way to do great work is to love what you do.", "productivity"),
    Quote("Dream big and dare to fail.", "creativity"),
    Quote("Take care of your body. It's the only place you have to live.", "wellness"),
    Quote("Simplicity is the ultimate sophistication.", "productivity"),
    Quote("Your limitation—it's only your imagination.", "creativity"),
    Quote("Every day is a second chance.", "wellness"),
]

# ---------------------------------------------------------------------------
# Core functionality
# ---------------------------------------------------------------------------

def _filter_quotes(category: Optional[str]) -> List[Quote]:
    """Return quotes matching *category* (or all if ``None``).

    Raises:
        ValueError: If a non‑None category is supplied but no quotes match.
    """
    if category is None:
        return _QUOTES
    filtered = [q for q in _QUOTES if q.category == category]
    if not filtered:
        raise ValueError(f"No quotes found for category '{category}'.")
    return filtered


def get_random_quote(category: Optional[str] = None, seed: Optional[int] = None) -> str:
    """Return a random quote string.

    Args:
        category: Optional category filter (e.g., ``"productivity"``).
        seed: Optional integer seed for deterministic output.
    """
    candidates = _filter_quotes(category)
    rng = random.Random(seed)  # deterministic when seed is provided
    chosen = rng.choice(candidates)
    return chosen.text

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="daily_motivation_quote",
        description="Print a random motivational quote.",
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Filter quotes by category (e.g., productivity, wellness, creativity).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Integer seed for deterministic output (useful for testing).",
    )
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    try:
        quote = get_random_quote(category=args.category, seed=args.seed)
        print(quote)
    except ValueError as exc:
        # In a CLI context we exit with a non‑zero status and print the error.
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
