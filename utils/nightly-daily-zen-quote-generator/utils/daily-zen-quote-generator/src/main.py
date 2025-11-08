import json
import sys
from datetime import date
from pathlib import Path
from typing import List, Dict

# Path to the bundled quotes JSON (relative to this file)
_QUOTES_PATH = Path(__file__).with_name('quotes.json')


def _load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains a single key ``"quote"``.
    """
    try:
        with _QUOTES_PATH.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError('Quotes JSON must be a list')
            return data
    except FileNotFoundError as exc:
        raise RuntimeError(f'Quotes file not found at {_QUOTES_PATH}') from exc


def get_quote(target_date: date | None = None) -> str:
    """Return the deterministic zen quote for *target_date*.

    Parameters
    ----------
    target_date: datetime.date, optional
        The date for which to fetch a quote. If ``None`` (default), uses ``date.today()``.

    Returns
    -------
    str
        The selected quote.
    """
    if target_date is None:
        target_date = date.today()
    quotes = _load_quotes()
    if not quotes:
        return "No quotes available."
    index = target_date.toordinal() % len(quotes)
    return quotes[index]["quote"]


def _cli() -> None:
    """Simple command‑line interface.

    Usage:
        python -m daily_zen_quote_generator          # prints today's quote
        python -m daily_zen_quote_generator 2023-04-01  # prints quote for given ISO date
    """
    if len(sys.argv) == 2:
        # User supplied a date string
        try:
            target_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print('Invalid date format. Use YYYY-MM-DD.', file=sys.stderr)
            sys.exit(1)
    else:
        target_date = None
    print(get_quote(target_date))


if __name__ == '__main__':
    _cli()
