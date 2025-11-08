import sys
import datetime
from typing import List

# A small curated list of Zen‑style quotes.
_QUOTES: List[str] = [
    "The river flows, but the stone remains.",
    "When the wind stops, the leaves still whisper.",
    "Silence is the loudest answer.",
    "A single step begins the longest journey.",
    "The moon watches both the night and the day.",
    "Empty cups hold the most tea.",
    "Mountains are patient, clouds are fleeting.",
    "Listen to the sound of your own breath.",
    "A candle does not fear the darkness.",
    "The seed knows the tree before it sprouts."
]


def _quote_for_date(date: datetime.date) -> str:
    """Return a deterministic quote based on the given date.

    The algorithm maps the ISO calendar day count to an index in the
    `_QUOTES` list, ensuring the same date always yields the same quote.
    """
    # Compute days since a fixed epoch (e.g., 2000‑01‑01) to get a stable integer.
    epoch = datetime.date(2000, 1, 1)
    days = (date - epoch).days
    index = days % len(_QUOTES)
    return _QUOTES[index]


def main(argv: List[str] | None = None) -> int:
    """Entry point for the CLI.

    Expected usage: `python -m daily_zen_quote <YYYY-MM-DD>`
    Returns exit code 0 on success, 1 on error.
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m daily_zen_quote <YYYY-MM-DD>")
        return 1
    try:
        input_date = datetime.datetime.strptime(argv[0], "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {argv[0]}. Expected YYYY-MM-DD.")
        return 1
    quote = _quote_for_date(input_date)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
