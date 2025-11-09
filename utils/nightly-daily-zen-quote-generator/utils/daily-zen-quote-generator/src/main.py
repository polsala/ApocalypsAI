import json
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict

_QUOTE_FILE = Path(__file__).with_name('quotes.json')


def _load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict has keys ``quote`` and ``author``.
    """
    with _QUOTE_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def _select_index(date: datetime.date, total: int) -> int:
    """Deterministically select an index based on the given date.

    The algorithm hashes the ISO‑formatted date string with SHA‑256 and
    interprets the hex digest as an integer. The result is reduced modulo
    ``total``.
    """
    date_str = date.isoformat()
    digest = hashlib.sha256(date_str.encode('utf-8')).hexdigest()
    return int(digest, 16) % total


def get_quote_of_the_day(date: datetime.date | None = None) -> Dict[str, str]:
    """Return the quote for *date* (defaults to today).

    Parameters
    ----------
    date: datetime.date | None
        The date for which to retrieve a quote. If ``None`` the current
        system date is used.

    Returns
    -------
    Dict[str, str]
        A mapping with ``quote`` and ``author`` keys.
    """
    if date is None:
        date = datetime.date.today()
    quotes = _load_quotes()
    if not quotes:
        raise RuntimeError('Quote list is empty')
    idx = _select_index(date, len(quotes))
    return quotes[idx]


def _format_quote(q: Dict[str, str]) -> str:
    return f"\"{q['quote']}\" — {q['author']}"


def main() -> None:
    quote = get_quote_of_the_day()
    print(_format_quote(quote))


if __name__ == "__main__":
    main()
