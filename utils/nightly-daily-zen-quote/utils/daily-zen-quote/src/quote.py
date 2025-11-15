"""daily_zen_quote – deterministic quote‑of‑the‑day utility.

Provides:
- :func:`get_quote` – return a quote for a given ``datetime.date`` (or today).
- CLI entry point when executed as ``python -m daily_zen_quote``.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path

# A small, curated list of Zen‑style sayings.
_QUOTES = [
    "The obstacle is the path.",
    "When the mind is still, the whole universe surrenders.",
    "Let go, or be dragged.",
    "Silence is a source of great strength.",
    "The journey itself is home.",
    "A single step is enough to begin.",
    "In the stillness, everything is revealed.",
    "Patience is the companion of wisdom.",
    "The moon does not fight the night; it simply shines.",
    "When you realize nothing is lacking, you have everything.",
]


def _index_for_date(date: datetime.date) -> int:
    """Return a stable index into ``_QUOTES`` based on ``date``.

    The algorithm uses the ordinal of the date (days since 0001‑01‑01) and
    wraps it modulo the number of quotes. This guarantees that the same date
    always maps to the same quote without any external state.
    """
    return date.toordinal() % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date (``datetime.date.today()``) is used.
    """
    if date is None:
        date = datetime.date.today()
    idx = _index_for_date(date)
    return _QUOTES[idx]


def _main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    _main()
