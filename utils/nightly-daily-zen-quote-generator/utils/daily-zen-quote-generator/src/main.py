import argparse
import datetime
from typing import List

# A small collection of zen‑like quotes. Feel free to extend.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "The only constant is change.",
    "Be present, not perfect.",
    "Nature does not hurry, yet everything is accomplished.",
    "Know the rules well, so you can break them effectively."
]


def _select_quote(date: datetime.date) -> str:
    """Select a quote deterministically based on the given date.

    The algorithm is simple: compute the ordinal of the date, take the modulo
    with the number of quotes, and return the quote at that index.
    """
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return the quote of the day.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    return _select_quote(date)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a deterministic Zen quote for today or a supplied date."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Optional date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args()


def _main() -> None:
    args = _parse_args()
    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        date = None
    quote = get_quote_of_the_day(date)
    print(quote)


if __name__ == "__main__":
    _main()
