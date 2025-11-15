import json
import datetime
import pathlib
import sys


def _quotes_path() -> pathlib.Path:
    """Return the absolute path to the bundled ``quotes.json`` file."""
    return pathlib.Path(__file__).with_name('quotes.json')


def load_quotes() -> list[str]:
    """Load the list of quotes from ``quotes.json``.

    Returns
    -------
    list[str]
        A list of quote strings.
    """
    path = _quotes_path()
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    The selection is deterministic: ``date.toordinal() % len(quotes)``.
    """
    if date is None:
        date = datetime.date.today()
    quotes = load_quotes()
    if not quotes:
        raise RuntimeError('No quotes available')
    index = date.toordinal() % len(quotes)
    return quotes[index]


def main() -> None:
    """CLI entry point – prints the quote of today to stdout."""
    quote = get_quote_of_the_day()
    print(quote)


if __name__ == '__main__':
    # Allow running the module directly via ``python -m daily_zen_quote_generator``
    # Adjust ``sys.path`` so the module can be imported when executed from the repo root.
    src_dir = pathlib.Path(__file__).parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    main()
