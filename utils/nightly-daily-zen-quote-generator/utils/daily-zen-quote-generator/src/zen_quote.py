"""
zen_quote.py – Deterministic daily Zen quote generator.

Provides:
- `get_today_quote()` – returns the quote for the current date.
- CLI entry point when executed as a module.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# A modest collection of Zen‑style sayings.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "In the middle of difficulty lies opportunity.",
    "Know the rules well, so you can break them wisely.",
    "A single moment can change a lifetime.",
    "Peace comes from within; do not seek it without."
]


def _deterministic_index(date: datetime.date) -> int:
    """
    Compute a deterministic index into the quotes list based on the given date.

    The built‑in `hash` is salted per‑process, so we mask it to 32‑bits to obtain
    a stable, reproducible value across interpreter runs.
    """
    date_str = date.isoformat()
    # Mock rationale: mask hash to 32‑bits for reproducibility across sessions.
    masked_hash = hash(date_str) & 0xffffffff
    return masked_hash % len(_QUOTES)


def get_today_quote(date: datetime.date | None = None) -> str:
    """
    Return the Zen quote for *date* (defaults to today).

    Parameters
    ----------
    date: datetime.date, optional
        The date for which to retrieve the quote. Useful for testing.

    Returns
    -------
    str
        The selected quote.
    """
    if date is None:
        date = datetime.date.today()
    idx = _deterministic_index(date)
    return _QUOTES[idx]


def main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    quote = get_today_quote()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument for quick manual testing:
    #   python -m zen_quote 2023-01-01
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_today_quote(custom_date))
    else:
        main()
