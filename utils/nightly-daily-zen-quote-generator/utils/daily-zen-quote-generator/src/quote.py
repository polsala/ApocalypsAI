import argparse
import datetime
from typing import List

# A modest collection of Zen‑style sayings.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the still water, the moon reflects.",
    "A single breath can change a lifetime.",
    "The bamboo that bends is stronger than the oak that resists.",
    "Empty your cup so it may be filled anew.",
    "When you realize nothing is lacking, the whole world belongs to you."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the deterministic Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is based on the day‑of‑year modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    # ``timetuple().tm_yday`` gives 1‑based day of year.
    day_of_year = date.timetuple().tm_yday
    index = (day_of_year - 1) % len(_QUOTES)
    return _QUOTES[index]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-generator",
        description="Print a deterministic Zen quote for today."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Optional date (YYYY-MM-DD) to retrieve the quote for. Defaults to today."
    )
    args = parser.parse_args()
    quote = get_quote(args.date)
    print(quote)


if __name__ == "__main__":
    _cli()
