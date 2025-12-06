import datetime
from typing import List

_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "The best way to predict the future is to invent it. – Alan Kay",
]


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date (or today).

    The quote is selected by taking the date's ordinal value modulo the number of
    available quotes. This approach requires no external resources and yields the
    same result for the same date on any platform.
    """
    if date is None:
        date = datetime.date.today()
    idx = date.toordinal() % len(_QUOTES)
    return _QUOTES[idx]
