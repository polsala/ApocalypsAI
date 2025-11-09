import json
import random
import pathlib
from typing import List, Dict

_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[Dict[str, str]]:
    """Load the bundled quotes JSON.

    Returns
    -------
    List[Dict[str, str]]
        A list where each item has ``"quote"`` and optional ``"author"`` keys.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("quotes", [])


def get_random_quote() -> str:
    """Return a formatted random quote.

    The function picks a random entry from the bundled list and formats it as
    ``"<quote>" – <author>`` when an author is present.
    """
    quotes = _load_quotes()
    if not quotes:
        raise RuntimeError("No quotes available.")
    entry = random.choice(quotes)
    quote = entry.get("quote", "")
    author = entry.get("author")
    if author:
        return f'"{quote}" – {author}'
    return f'"{quote}"'


def main() -> None:
    """CLI entry point – prints a random quote to stdout."""
    print(get_random_quote())


if __name__ == "__main__":
    main()
