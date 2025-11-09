import argparse
import json
import random
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Path to the bundled quotes file (relative to this file)
_QUOTES_PATH = Path(__file__).with_name("quotes.json")


def load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict has keys ``text`` and ``author``.
    """
    try:
        with _QUOTES_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("quotes.json must contain a list")
            return data
    except FileNotFoundError as exc:
        raise RuntimeError(f"Quotes file not found at {_QUOTES_PATH}") from exc


def filter_quotes(quotes: List[Dict[str, str]], author: Optional[str]) -> List[Dict[str, str]]:
    """Return quotes matching *author* if provided, otherwise the full list.
    """
    if author is None:
        return quotes
    lowered = author.lower()
    return [q for q in quotes if q.get("author", "").lower() == lowered]


def get_random_quote(author: Optional[str] = None) -> Dict[str, str]:
    """Pick a random quote, optionally limited to a specific author.

    Parameters
    ----------
    author: Optional[str]
        If supplied, only quotes by this author are considered.

    Returns
    -------
    Dict[str, str]
        A dict with ``text`` and ``author`` keys.
    """
    quotes = load_quotes()
    filtered = filter_quotes(quotes, author)
    if not filtered:
        raise ValueError(f"No quotes found for author: {author!r}")
    return random.choice(filtered)


def format_quote(quote: Dict[str, str]) -> str:
    """Return a pretty‑printed string for a quote dict.
    """
    text = quote.get("text", "")
    author = quote.get("author", "Unknown")
    return f"\"{text}\" — {author}"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--author",
        help="Filter quotes by author name (case‑insensitive)",
        type=str,
        default=None,
    )
    args = parser.parse_args(argv)
    try:
        quote = get_random_quote(author=args.author)
        print(format_quote(quote))
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
