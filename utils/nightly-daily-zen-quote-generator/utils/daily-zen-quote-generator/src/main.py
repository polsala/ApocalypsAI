"""Daily Zen Quote Generator"""

import json
import sys
from datetime import date
from pathlib import Path

_QUOTE_FILE = Path(__file__).with_name("quotes.json")


def load_quotes() -> list[str]:
    """Load quotes from the bundled JSON file."""
    try:
        with _QUOTE_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise RuntimeError(f"Failed to load quotes: {exc}") from exc


def get_quote(target_date: date | None = None) -> str:
    """Return the quote for the given date (or today if ``None``)."""
    quotes = load_quotes()
    if not quotes:
        raise ValueError("Quote list is empty")
    today = target_date or date.today()
    index = today.toordinal() % len(quotes)
    return quotes[index]


def main() -> None:
    """CLI entry point."""
    try:
        quote = get_quote()
        print(quote)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
