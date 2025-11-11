import hashlib
import datetime
from typing import List

# Embedded list of Zen quotes (feel free to extend)
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single moment can change a lifetime.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "Know the rules so you can break them wisely."
]


def _hash_date(date_str: str) -> int:
    """Return a stable integer hash for a given ISO date string.

    We use SHA‑256 and convert the first 8 hex digits to an int.
    """
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def get_quote_of_day(today: datetime.date | None = None) -> str:
    """Return the Zen quote for *today*.

    Parameters
    ----------
    today: datetime.date, optional
        Allows injection of a specific date (useful for testing). If ``None``
        the current UTC date is used.
    """
    if today is None:
        today = datetime.date.today()
    date_str = today.isoformat()
    idx = _hash_date(date_str) % len(_QUOTES)
    return _QUOTES[idx]


def main() -> None:
    """CLI entry point – prints the quote of the day to stdout."""
    quote = get_quote_of_day()
    print(quote)


if __name__ == "__main__":
    main()
