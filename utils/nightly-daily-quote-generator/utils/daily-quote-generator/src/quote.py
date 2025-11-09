"""daily_quote_generator – deterministic Quote of the Day.

Provides a simple CLI (`python -m daily_quote_generator`) that prints a whimsical quote
based on the current date. The selection algorithm is deterministic and requires no
network access, making it safe for offline CI runs.
"""

from __future__ import annotations

import datetime
import hashlib
import sys
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Quote data – feel free to extend this list. The order is intentional because
# the selection algorithm uses the index modulo the length of the list.
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and it gave me a coffee break error.",
    "Life is short – smile while you still have teeth.",
    "To err is human; to really mess things up you need a computer.",
    "I would tell you a UDP joke, but you might not get it.",
    "Debugging: Removing the needles from the haystack, one at a time.",
    "The universe is made of protons, neutrons, electrons, and morons.",
]


def _date_string(date: datetime.date) -> str:
    """Return an ISO‑format string for *date*.

    Separated into its own function to ease testing/mocking.
    """
    return date.isoformat()


def _hash_date(date_str: str) -> int:
    """Hash *date_str* with SHA‑256 and return an integer.

    Using a cryptographic hash guarantees a uniform distribution across the
    quote list regardless of the date pattern.
    """
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the current local date is used.
    The function is pure and deterministic – given the same *date* it always
    returns the same quote.
    """
    if date is None:
        date = datetime.date.today()
    date_str = _date_string(date)
    hashed = _hash_date(date_str)
    index = hashed % len(_QUOTES)
    return _QUOTES[index]


def _cli() -> None:
    """Entry‑point for ``python -m daily_quote_generator``.

    Prints the quote for today to ``stdout``.
    """
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # When executed as a module, act as a tiny CLI.
    _cli()
