import json
import pathlib
import datetime
import sys

def load_quotes() -> list[str]:
    """Load quotes from the bundled JSON file."""
    quotes_path = pathlib.Path(__file__).with_name("quotes.json")
    with quotes_path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["quotes"]

def quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date (defaults to today)."""
    if date is None:
        date = datetime.date.today()
    quotes = load_quotes()
    if not quotes:
        raise ValueError("No quotes available")
    index = (date.timetuple().tm_yday - 1) % len(quotes)
    return quotes[index]

def main() -> None:
    """CLI entry point."""
    print(quote_of_the_day())

if __name__ == "__main__":
    main()
