import json
import random
import pathlib
from typing import List

_QUOTE_FILE = pathlib.Path(__file__).with_name('quotes.json')


def _load_quotes() -> List[str]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[str]
        A list of quote strings.
    """
    with _QUOTE_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # Expecting a JSON array of strings.
    return data


def get_random_quote() -> str:
    """Return a random quote from the bundled list.

    The function is deliberately simple – it loads the quotes each call to keep the
    utility self‑contained and easy to test with mocks.
    """
    quotes = _load_quotes()
    if not quotes:
        raise ValueError('Quote list is empty')
    return random.choice(quotes)


def main() -> None:
    """CLI entry point – prints a random quote to stdout."""
    print(get_random_quote())


if __name__ == '__main__':
    main()
