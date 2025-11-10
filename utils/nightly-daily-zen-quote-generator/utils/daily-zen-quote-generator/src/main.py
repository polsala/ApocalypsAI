import datetime
import sys
from typing import List

# A small curated list of Zen‑like quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "What you think, you become.",
    "Simplicity is the ultimate sophistication.",
    "Be yourself; everyone else is already taken.",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the current local date is used. The quote is selected
    deterministically by taking the ordinal of the date modulo the number of
    available quotes.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    """CLI entry‑point: print today's quote to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Allow ``python -m daily_zen_quote_generator`` to work when the package is
    # executed as a module.
    main()
