import json
import pathlib
import argparse
import datetime
import hashlib
from typing import List

# Path to the JSON file containing quotes (relative to this file)
_QUOTE_FILE = pathlib.Path(__file__).resolve().parent.parent / "data" / "quotes.json"


def _load_quotes() -> List[str]:
    """Load the list of quotes from the JSON file.

    Returns
    -------
    List[str]
        A list of quote strings.
    """
    with open(_QUOTE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Expecting a JSON array of strings
    return data


def _date_to_key(date: datetime.date) -> int:
    """Convert a date to a deterministic integer key.

    The function hashes the ISO representation of the date and returns an
    integer derived from the first 8 bytes of the SHA‑256 digest.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).digest()
    # Use int.from_bytes to get a reproducible integer
    return int.from_bytes(digest[:8], "big")


def get_today_quote(date: datetime.date | None = None) -> str:
    """Return the quote for the given date (or today if ``None``).

    Parameters
    ----------
    date: datetime.date | None
        The date for which to fetch a quote. If ``None``, uses ``datetime.date.today()``.

    Returns
    -------
    str
        The selected quote.
    """
    if date is None:
        date = datetime.date.today()
    quotes = _load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty.")
    key = _date_to_key(date)
    index = key % len(quotes)
    return quotes[index]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic zen quote for a given date.")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="ISO date (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    print(get_today_quote(args.date))
