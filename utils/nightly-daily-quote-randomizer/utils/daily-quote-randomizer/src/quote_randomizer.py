import json
import random
import pathlib
from typing import Optional, Dict, List

# Path to the bundled quotes JSON file
_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[Dict]:
    """Load quotes from the bundled JSON file."""
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_random_quote(tag: Optional[str] = None) -> Dict:
    """
    Return a random quote.

    Parameters
    ----------
    tag : str, optional
        If provided, only quotes containing this tag are considered.

    Returns
    -------
    dict
        A dictionary with keys: 'text', 'author', 'tags'.
    """
    quotes = _load_quotes()
    if tag:
        filtered = [q for q in quotes if tag.lower() in (t.lower() for t in q.get("tags", []))]
        if not filtered:
            raise ValueError(f"No quotes found with tag '{tag}'.")
        quotes = filtered
    # Randomly select a quote
    return random.choice(quotes)


def main() -> None:
    """CLI entry point."""
    try:
        quote = get_random_quote()
        print(f"{quote['text']} — {quote['author']}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
