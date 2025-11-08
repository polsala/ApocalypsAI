import sys
import datetime
from typing import List

# A small collection of Zen‑style quotes.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with a single step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "Nature does not hurry, yet everything is accomplished.",
    "To know the road ahead, ask those who have traveled it.",
    "A candle loses nothing by lighting another candle.",
    "The softest thing in the universe overcomes the hardest thing in the universe."
]


def _deterministic_index(date: datetime.date) -> int:
    """Return a deterministic index into the quotes list based on the date.

    The algorithm is simple: convert the date to an integer ``YYYYMMDD`` and
    take the modulo with the number of quotes.
    """
    date_int = int(date.strftime("%Y%m%d"))
    return date_int % len(_QUOTES)


def get_quote(date: datetime.date) -> str:
    """Return the Zen quote for *date*.

    Parameters
    ----------
    date: datetime.date
        The date for which to retrieve a quote.

    Returns
    -------
    str
        The selected quote.
    """
    idx = _deterministic_index(date)
    return _QUOTES[idx]


def _parse_date(arg: str) -> datetime.date:
    """Parse a ``YYYY-MM-DD`` string into a :class:`datetime.date`.

    Raises ``ValueError`` if the format is invalid.
    """
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d").date()
    except Exception as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc


def main(argv: List[str] | None = None) -> None:
    """CLI entry point.

    Usage:
        python -m utils.daily-zen-quote-generator.src.main [YYYY-MM-DD]
    If no date is provided, today's date is used.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        target_date = datetime.date.today()
    else:
        target_date = _parse_date(argv[0])

    quote = get_quote(target_date)
    print(f"\"{quote}\"")


if __name__ == "__main__":
    main()
