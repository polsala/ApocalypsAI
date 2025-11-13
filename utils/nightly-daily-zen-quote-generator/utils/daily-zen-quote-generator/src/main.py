import json
import pathlib
import datetime
import sys

_QUOTE_FILE = pathlib.Path(__file__).with_name('quotes.json')


def _load_quotes() -> list[str]:
    """Load the built‑in list of quotes from ``quotes.json``.

    Returns
    -------
    list[str]
        A list of quote strings.
    """
    with _QUOTE_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection algorithm is deterministic: ``date.toordinal() % len(quotes)``.
    """
    if date is None:
        date = datetime.date.today()
    quotes = _load_quotes()
    index = date.toordinal() % len(quotes)
    return quotes[index]


def main() -> None:
    """CLI entry point – prints the quote for today to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == '__main__':
    # Allow ``python -m daily_zen_quote_generator`` when the package is executed as a module.
    # ``__package__`` will be ``None`` in that case, so we adjust ``sys.path`` to import ``src``.
    if __package__ is None:
        # Add the parent directory (which contains ``src``) to ``sys.path``.
        parent = pathlib.Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(parent))
    main()
