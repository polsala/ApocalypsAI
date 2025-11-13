import json
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict

# Path to the bundled quotes JSON file
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "quotes.json"


def load_quotes() -> List[Dict[str, str]]:
    """Load quotes from the bundled JSON file."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _hash_date(date_str: str) -> int:
    """Return an integer hash of the date string using SHA‑256."""
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16)


def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    If ``date`` is ``None`` the function uses ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    quotes = load_quotes()
    if not quotes:
        raise ValueError("No quotes available.")
    idx = _hash_date(date.isoformat()) % len(quotes)
    selected = quotes[idx]
    return f"{selected['quote']} — {selected['author']}"


def main() -> None:
    """CLI entry point that prints today's quote."""
    print(get_quote())


if __name__ == "__main__":
    main()
