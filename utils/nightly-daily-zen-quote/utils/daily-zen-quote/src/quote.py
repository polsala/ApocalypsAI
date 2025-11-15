import datetime
from typing import List

# A small curated list of Zen‑like quotes.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Be yourself; everyone else is already taken.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
]


def get_zen_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date*.

    If *date* is ``None`` the current local date is used. The quote is chosen
    deterministically by indexing the ``_QUOTES`` list with ``date.toordinal()``
    modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry‑point: print today's Zen quote to stdout."""
    print(get_zen_quote())


if __name__ == "__main__":
    main()
