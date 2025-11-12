import datetime
import sys

# A small curated list of zen‑like sayings.
QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "What you do today can improve all your tomorrows.",
    "Simplicity is the ultimate sophistication.",
    "Stay hungry, stay foolish.",
    "In the middle of difficulty lies opportunity.",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is deterministic: ``date.toordinal() % len(QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    """CLI entry‑point – prints today’s quote to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Allow the module to be executed directly: ``python -m src.main``
    main()
