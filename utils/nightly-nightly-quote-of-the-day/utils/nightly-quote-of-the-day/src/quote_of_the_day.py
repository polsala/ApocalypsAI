'''Quote of the Day utility.

Provides a deterministic quote based on the day of the year.
'''

from __future__ import annotations

import datetime
from typing import List

_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "The best way to predict the future is to invent it. – Alan Kay",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "The journey of a thousand miles begins with one step. – Lao Tzu",
    "What we think, we become. – Buddha",
    "Dream big and dare to fail. – Norman Vaughan",
    "Stay hungry, stay foolish. – Steve Jobs",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for the given date.

    If *date* is ``None`` the current local date is used.
    The quote is selected by taking the day of year modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    index = day_of_year % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """Print today's quote to stdout."""
    print(get_quote())


if __name__ == "__main__":
    main()
