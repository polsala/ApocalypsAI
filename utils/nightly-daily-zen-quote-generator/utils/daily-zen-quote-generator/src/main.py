import argparse
import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go or be dragged.",
    "The obstacle is the path.",
]


def _select_quote(date: datetime.date) -> str:
    """Deterministic selection based on days since Unix epoch."""
    days = (date - datetime.date(1970, 1, 1)).days
    index = days % len(_QUOTES)
    return _QUOTES[index]


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date (defaults to today)."""
    if date is None:
        date = datetime.date.today()
    return _select_quote(date)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a deterministic Zen quote for today."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Specify a date (YYYY-MM-DD) instead of today.",
    )
    args = parser.parse_args()
    quote = get_quote_of_the_day(args.date)
    print(quote)


if __name__ == "__main__":
    main()
