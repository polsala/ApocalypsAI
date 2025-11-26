import sys
import datetime
from typing import List

# A modest collection of inspirational quotes.
_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Get busy living or get busy dying. – Stephen King",
    "You have within you right now, everything you need to deal with whatever the world can throw at you. – Brian Tracy",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The future belongs to those who prepare for it today. – Malcolm X",
    "Do not watch the clock. Do what it does. Keep going. – Sam Levenson",
    "Everything you can imagine is real. – Pablo Picasso",
    "The best way to predict the future is to invent it. – Alan Kay",
]


def get_quote_for_date(date: datetime.date) -> str:
    """Return a deterministic quote for the given date.

    The selection is based on the day of the year (1‑365/366) and wraps
    around the length of the quote list.
    """
    day_of_year = date.timetuple().tm_yday
    index = (day_of_year - 1) % len(_QUOTES)
    return _QUOTES[index]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the quote for today to stdout. Returns exit code 0.
    """
    today = datetime.date.today()
    quote = get_quote_for_date(today)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
