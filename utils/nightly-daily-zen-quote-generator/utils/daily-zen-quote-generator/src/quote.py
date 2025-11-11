import json
import hashlib
import datetime
from pathlib import Path
from typing import List

_QUOTE_FILE = Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[str]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[str]
        A list of quote strings.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # Expecting a JSON array of strings
    return data


def _select_index(date_str: str, count: int) -> int:
    """Deterministically map a date string to an index.

    Parameters
    ----------
    date_str: str
        ISO formatted date (e.g., "2025-11-11").
    count: int
        Number of available quotes.

    Returns
    -------
    int
        Index in the range ``0 <= idx < count``.
    """
    # Use SHA‑256 for a stable hash across Python versions
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    # Convert a portion of the hex digest to an int
    num = int(digest[:8], 16)
    return num % count


def get_quote_of_day(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date (or today if omitted).

    The function is deterministic: the same date always yields the same quote.

    Parameters
    ----------
    date: datetime.date | None, optional
        The date for which to retrieve a quote. Defaults to ``datetime.date.today()``.

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
    idx = _select_index(date.isoformat(), len(quotes))
    return quotes[idx]


def main() -> None:
    """CLI entry point: print today's quote to stdout."""
    print(get_quote_of_day())


if __name__ == "__main__":
    main()
