'''\
Daily Zen Quote Generator.

Provides `get_quote_of_day(date: datetime.date | None = None) -> str`.
'''\

from __future__ import annotations
import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "Less is more.",
    "Stay hungry, stay foolish.",
    "Do not watch the clock. Do what it does. Keep going.",
    "Dream big and dare to fail."
]


def get_quote_of_day(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    The quote is selected by taking the ordinal of the date modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


if __name__ == "__main__":
    print(get_quote_of_day())
