"""quote_of_the_day
~~~~~~~~~~~~~~~~~~
Utility that returns a deterministic quote based on the current date.

All data is stored locally; no external network access is required.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# Static quote database
# ---------------------------------------------------------------------------
QUOTES: List[Dict[str, List[str] | str]] = [
    {"text": "The only limit to our realization of tomorrow is our doubts of today.", "tags": ["inspiration"]},
    {"text": "I have not failed. I've just found 10,000 ways that won't work.", "tags": ["humor", "inspiration"]},
    {"text": "Life is what happens when you're busy making other plans.", "tags": ["philosophy"]},
    {"text": "If you think you are too small to make a difference, try sleeping with a mosquito.", "tags": ["humor"]},
    {"text": "The purpose of our lives is to be happy.", "tags": ["inspiration"]},
]


def _filter_quotes(tag: Optional[str]) -> List[Dict[str, List[str] | str]]:
    """Return quotes matching *tag* (or all if *tag* is None)."""
    if tag is None:
        return QUOTES
    filtered = [q for q in QUOTES if tag.lower() in (t.lower() for t in q["tags"])]
    return filtered


def get_quote(tag: Optional[str] = None, today: Optional[datetime.date] = None) -> str:
    """Return a deterministic quote for *today* (defaults to ``date.today()``).

    The quote is selected by taking the ordinal of the date modulo the number of
    available quotes (after optional tag filtering).

    Args:
        tag: Optional tag to filter quotes.
        today: Optional date to use instead of ``datetime.date.today()`` – useful
            for testing.
    Raises:
        ValueError: If no quotes match the supplied tag.
    """
    if today is None:
        today = datetime.date.today()
    candidates = _filter_quotes(tag)
    if not candidates:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    index = today.toordinal() % len(candidates)
    return candidates[index]["text"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a deterministic Quote of the Day.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., 'humor', 'inspiration').",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)
    try:
        quote = get_quote(tag=args.tag)
        print(quote)
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
