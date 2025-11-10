import json
import pathlib
import datetime
from typing import List, Optional

# Path to the bundled JSON file containing quotes
_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[str]:
    """Load quotes from the bundled JSON file.

    Returns a list of quote strings. Raises ``ValueError`` if the file cannot be read
    or does not contain a list.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("quotes.json must contain a JSON array of strings")
    return data

# Cache the quotes after the first load to avoid repeated I/O.
_QUOTES_CACHE: Optional[List[str]] = None


def get_daily_quote(date: Optional[datetime.date] = None) -> str:
    """Return a deterministic quote for the given ``date``.

    If ``date`` is ``None`` the current local date is used. The quote is selected by
    taking the day‑of‑year (1‑based) modulo the number of available quotes.
    """
    global _QUOTES_CACHE
    if _QUOTES_CACHE is None:
        _QUOTES_CACHE = _load_quotes()
    if not _QUOTES_CACHE:
        raise ValueError("No quotes available.")
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    # Subtract 1 because Jan 1 is day 1 but list indices start at 0
    index = (day_of_year - 1) % len(_QUOTES_CACHE)
    return _QUOTES_CACHE[index]


def main() -> None:
    """CLI entry point: print today's Zen quote to stdout."""
    print(get_daily_quote())


if __name__ == "__main__":
    main()
