"""Daily Zen Quote Generator.

Provides a deterministic quote of the day from a built‑in list.
"""

import argparse
import datetime
import json
import pathlib
import sys
from typing import List, Dict

_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")


def load_quotes() -> List[Dict[str, str]]:
    """Load quotes from the bundled JSON file."""
    try:
        data = _QUOTE_FILE.read_text(encoding="utf-8")
        return json.loads(data)
    except Exception as exc:
        raise RuntimeError(f"Failed to load quotes: {exc}") from exc


def get_quote_of_day(date: datetime.date | None = None) -> Dict[str, str]:
    """Return a quote dict for the given date (or today).

    Selection is deterministic: index = ordinal(date) % len(quotes).
    """
    if date is None:
        date = datetime.date.today()
    quotes = load_quotes()
    if not quotes:
        raise RuntimeError("Quote list is empty.")
    index = date.toordinal() % len(quotes)
    return quotes[index]


def format_quote(quote: Dict[str, str]) -> str:
    """Pretty‑print a quote."""
    return f"“{quote['quote']}” — {quote['author']}"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a deterministic quote of the day."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Optional date (YYYY-MM-DD) to fetch the quote for.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        quote = get_quote_of_day(args.date)
        print(format_quote(quote))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
