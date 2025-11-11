import json
import datetime
import pathlib
from typing import Dict, List

_QUOTE_FILE = pathlib.Path(__file__).with_name('quotes.json')
_EPOCH = datetime.date(1970, 1, 1)  # Fixed reference point


def _load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict has keys ``text`` and ``author``.
    """
    raw = _QUOTE_FILE.read_text(encoding='utf-8')
    return json.loads(raw)


def get_quote_of_day(today: datetime.date | None = None) -> str:
    """Return the quote for *today*.

    Parameters
    ----------
    today: datetime.date | None, optional
        Allows injection of a custom date (used by tests). If ``None`` the
        current UTC date is used.

    Returns
    -------
    str
        Formatted quote, e.g. ``"Do something" – Author``.
    """
    if today is None:
        today = datetime.date.today()
    quotes = _load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty")
    # Days since epoch determines the index
    delta_days = (today - _EPOCH).days
    idx = delta_days % len(quotes)
    quote = quotes[idx]
    return f"\"{quote['text']}\" – {quote['author']}"


def _cli() -> None:
    """Simple command‑line entry point.
    """
    print(get_quote_of_day())


if __name__ == "__main__":
    _cli()
