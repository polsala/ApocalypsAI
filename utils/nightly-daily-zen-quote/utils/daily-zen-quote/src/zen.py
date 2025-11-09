"""daily_zen_quote – deterministic Zen quote provider.

This module contains a small, hard‑coded list of Zen‑style quotes. The function
`get_quote` selects a quote based on the supplied date (or today if omitted).
The selection algorithm is deterministic: it uses the ordinal of the date
modulo the number of quotes.

The module also provides a tiny CLI for convenience.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Quote data – kept small to stay self‑contained. Feel free to extend.
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with a single step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single moment can change a lifetime.",
    "Nature does not hurry, yet everything is accomplished.",
    "The softest thing in the world beats the hardest.",
    "When you realize nothing is lacking, the whole world belongs to you."
]


def _load_quotes() -> List[str]:
    """Return the list of quotes.

    In a real‑world utility this could read from a JSON/YAML file, but keeping the
    list in‑code guarantees offline operation and eliminates I/O for the tests.
    """
    # Mock rationale: returning a constant list ensures deterministic behaviour.
    return _QUOTES


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The quote index is calculated as ``date.toordinal() % len(quotes)``.
    """
    if date is None:
        date = datetime.date.today()
    quotes = _load_quotes()
    index = date.toordinal() % len(quotes)
    return quotes[index]


def _parse_cli_args(args: List[str]) -> datetime.date | None:
    """Parse optional date argument from CLI.

    Expected format: ``YYYY-MM-DD``. Returns ``None`` if no argument is supplied.
    """
    if not args:
        return None
    try:
        return datetime.datetime.strptime(args[0], "%Y-%m-%d").date()
    except ValueError as exc:
        print(f"Invalid date format: {args[0]!r}. Expected YYYY-MM-DD.", file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> None:
    """CLI entry point.

    Usage:
        python -m daily_zen_quote [optional-date]
    """
    date = _parse_cli_args(sys.argv[1:])
    quote = get_quote(date)
    print(quote)


if __name__ == "__main__":
    main()
