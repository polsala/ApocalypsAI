import datetime
from typing import Optional

_QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the illusion of control.",
    "Silence is the language of the soul.",
]


def _select_quote_for_date(date: datetime.date) -> str:
    """Deterministically pick a quote based on the given date.

    The algorithm uses the date's ordinal (days since 0001‑01‑01) and
    takes the modulo with the number of available quotes.
    """
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def get_quote(date: Optional[datetime.date] = None) -> str:
    """Return the Zen quote for *date* (defaults to today)."""
    if date is None:
        date = datetime.date.today()
    return _select_quote_for_date(date)


if __name__ == "__main__":
    print(get_quote())
