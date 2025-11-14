"""daily_zen_quote_generator – deterministic Zen quotes.

Provides a single public function:

    get_daily_zen_quote(date: Optional[datetime.date] = None) -> str

If *date* is omitted, the current UTC date is used.
"""

from __future__ import annotations

import datetime
import hashlib
from typing import List, Optional

# A curated list of Zen‑style quotes. Feel free to extend.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with a single step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single breath can change a lifetime.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "Know the rules well, so you can break them wisely.",
]


def _deterministic_index(date: datetime.date) -> int:
    """Return a reproducible index into ``_QUOTES`` for *date*.

    The algorithm hashes the ISO‑format date string and maps it into the
    range ``0 .. len(_QUOTES) - 1``. This ensures the same date always yields
    the same quote without any external state.
    """
    # Convert date to a stable string representation.
    date_str = date.isoformat()
    # Compute a SHA‑256 hash – deterministic and uniform.
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    # Use the first 8 hex digits as an integer.
    num = int(digest[:8], 16)
    return num % len(_QUOTES)


def get_daily_zen_quote(date: Optional[datetime.date] = None) -> str:
    """Return the Zen quote for *date* (or today if ``None``).

    Parameters
    ----------
    date:
        A ``datetime.date`` object. If omitted, ``datetime.date.today()`` in UTC
        is used.

    Returns
    -------
    str
        The selected quote.
    """
    if date is None:
        # Use UTC today to avoid timezone surprises.
        date = datetime.datetime.utcnow().date()
    index = _deterministic_index(date)
    return _QUOTES[index]


if __name__ == "__main__":
    # Simple CLI entry point.
    print(get_daily_zen_quote())
