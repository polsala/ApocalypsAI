import datetime
from typing import List

# A curated list of short Zen quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Know the rules well, so you can break them.",
    "A single moment can change a lifetime.",
    "Nature does not hurry, yet everything is accomplished.",
    "Peace comes from within; do not seek it elsewhere."
]


def _select_index(date: datetime.date) -> int:
    """Return the index of the quote for a given date.

    The algorithm is deterministic: it uses the ordinal of the date (the number of days
    since 0001‑01‑01) modulo the number of available quotes.
    """
    return date.toordinal() % len(QUOTES)


def get_daily_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    index = _select_index(date)
    return QUOTES[index]


if __name__ == "__main__":
    # When executed as a script, print today's quote.
    print(get_daily_quote())
