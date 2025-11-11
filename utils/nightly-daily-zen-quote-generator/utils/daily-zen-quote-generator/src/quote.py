import json
import pathlib
import datetime
from typing import List

# Path to the bundled quotes JSON (relative to this file)
_QUOTES_PATH = pathlib.Path(__file__).with_name("../data/quotes.json").resolve()


def _load_quotes() -> List[str]:
    """Load the list of quotes from the JSON file.

    Returns
    -------
    List[str]
        A list of quote strings.
    """
    with open(_QUOTES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # The JSON is expected to be a list of strings.
    return data

# Cache quotes at import time – cheap and avoids repeated I/O.
_QUOTES = _load_quotes()


def _index_for_date(date: datetime.date) -> int:
    """Deterministically map a date to an index in the quotes list.

    The algorithm is simple: take the ISO calendar week number and day of year,
    combine them, and modulo by the number of quotes.
    """
    # Combine year, month, day into a reproducible integer.
    seed = int(date.strftime("%Y%m%d"))
    return seed % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for *date* (defaults to today).

    Parameters
    ----------
    date: datetime.date | None, optional
        The date for which to retrieve a quote. If ``None`` the current local
        date is used.

    Returns
    -------
    str
        The selected quote.
    """
    if date is None:
        date = datetime.date.today()
    idx = _index_for_date(date)
    return _QUOTES[idx]


def main() -> None:
    """CLI entry‑point – prints today's quote to stdout."""
    print(get_quote())


if __name__ == "__main__":
    main()
