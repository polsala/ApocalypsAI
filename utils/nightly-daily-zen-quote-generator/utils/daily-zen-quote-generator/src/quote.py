import json
import pathlib
import datetime
from typing import Dict, List

_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")

def _load_quotes() -> List[Dict[str, str]]:
    """Load the bundled quotes JSON.

    Returns
    -------
    List[Dict[str, str]]
        Each dict has ``text`` and ``author`` keys.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

_QUOTES_CACHE: List[Dict[str, str]] | None = None

def _get_quotes() -> List[Dict[str, str]]:
    global _QUOTES_CACHE
    if _QUOTES_CACHE is None:
        _QUOTES_CACHE = _load_quotes()
    return _QUOTES_CACHE

def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for *date*.

    Parameters
    ----------
    date: datetime.date | None
        The date to base the quote on. If ``None`` (default), uses ``datetime.date.today()``.

    Returns
    -------
    str
        Formatted quote, e.g. ``"The journey..." – Lao Tzu``.
    """
    if date is None:
        date = datetime.date.today()
    quotes = _get_quotes()
    if not quotes:
        raise RuntimeError("No quotes available.")
    # Deterministic index based on the ordinal of the date.
    idx = date.toordinal() % len(quotes)
    q = quotes[idx]
    return f"\"{q['text']}\" – {q['author']}"

def main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    print(get_quote())

if __name__ == "__main__":
    main()
