"""Daily Zen Quote Generator.

Provides a CLI to print a random zen quote from a bundled list.
"""

import json
import random
import sys
from pathlib import Path

# Path to the bundled quotes JSON file (located in the same directory)
_QUOTES_PATH = Path(__file__).with_name("quotes.json")

def load_quotes() -> list[str]:
    """Load the list of quotes from the JSON file."""
    with _QUOTES_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quotes"]

def get_random_quote() -> str:
    """Return a random quote from the bundled list."""
    quotes = load_quotes()
    return random.choice(quotes)

def main() -> None:
    """CLI entry point."""
    quote = get_random_quote()
    print(quote)

if __name__ == "__main__":
    main()
