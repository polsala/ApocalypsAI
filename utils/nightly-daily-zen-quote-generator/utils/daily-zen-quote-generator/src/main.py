import argparse
import json
import random
import sys
from pathlib import Path

QUOTES_PATH = Path(__file__).with_name('quotes.json')


def load_quotes() -> list[dict]:
    """Load the bundled quotes JSON file.

    Returns
    -------
    list[dict]
        Each dict contains ``text``, ``author`` and optional ``category``.
    """
    try:
        with open(QUOTES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        sys.stderr.write('Quotes file not found.\n')
        sys.exit(1)
    except json.JSONDecodeError:
        sys.stderr.write('Quotes file is malformed.\n')
        sys.exit(1)


def pick_quote(quotes: list[dict], category: str | None = None) -> dict:
    """Select a random quote, optionally filtered by *category*.

    Parameters
    ----------
    quotes: list[dict]
        The full list of quote dictionaries.
    category: str | None
        If provided, only quotes whose ``category`` matches (case‑insensitive) are considered.
    """
    if category:
        filtered = [q for q in quotes if q.get('category', '').lower() == category.lower()]
        if not filtered:
            sys.stderr.write(f'No quotes found for category "{category}".\n')
            sys.exit(1)
        quotes = filtered
    return random.choice(quotes)


def format_quote(quote: dict) -> str:
    author = quote.get('author', 'Unknown')
    return f"\"{quote['text']}\" — {author}"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Print a random Zen quote.')
    parser.add_argument('--category', help='Filter quotes by category (e.g., mindfulness, humor)')
    args = parser.parse_args(argv)

    quotes = load_quotes()
    selected = pick_quote(quotes, args.category)
    print(format_quote(selected))


if __name__ == '__main__':
    main()
