"""Daily Zen Quote Generator.

Provides a deterministic quote based on the given date.
"""

from __future__ import annotations

import datetime
from typing import List

# Mock rationale: a short, uplifting list of quotes.
QUOTES: List[str] = [
    "Be yourself.",
    "Stay hungry.",
    "Embrace change.",
    "Keep it simple.",
    "Dream big."
]

def get_quote(date: datetime.date | None = None) -> str:
    """Return a Zen quote for the given date.

    If *date* is None, uses today's date.
    The quote is selected by taking the ordinal of the date modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(QUOTES)
    return QUOTES[index]

if __name__ == "__main__":
    print(get_quote())
