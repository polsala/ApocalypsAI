import json
import datetime
import sys
from pathlib import Path

QUOTES_PATH = Path(__file__).with_name("quotes.json")

def load_quotes() -> list[str]:
    """Load the list of quotes from the JSON file."""
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quotes"]

def get_quote(date: datetime.date | None = None) -> str:
    """Return the deterministic quote for *date*.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    quotes = load_quotes()
    if not quotes:
        raise ValueError("No quotes available")
    # ``tm_yday`` is 1‑based; subtract 1 for zero‑based indexing.
    index = (date.timetuple().tm_yday - 1) % len(quotes)
    return quotes[index]

def main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    quote = get_quote()
    print(quote)

if __name__ == "__main__":
    main()
