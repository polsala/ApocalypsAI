import sys
import datetime
import hashlib
from typing import List

# A small curated list of motivational quotes.
_QUOTES: List[str] = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "The best time to plant a tree was 20 years ago. The second best time is now. – Chinese Proverb",
    "Your limitation—it's only your imagination.",
    "Dream it. Wish it. Do it."
]


def _select_quote_for_date(target_date: datetime.date) -> str:
    """Deterministically select a quote based on the given date.

    The function hashes the ISO string of the date, converts the hash to an integer,
    and uses modulo arithmetic to pick an index from the _QUOTES list.
    """
    iso_str = target_date.isoformat()
    # Use SHA256 for stable hashing across Python versions.
    digest = hashlib.sha256(iso_str.encode("utf-8")).hexdigest()
    idx = int(digest, 16) % len(_QUOTES)
    return _QUOTES[idx]


def get_motivation(date: datetime.date | None = None) -> str:
    """Public API: return a motivational quote for *date* (or today).

    Parameters
    ----------
    date: datetime.date | None
        The date for which to retrieve a quote. If ``None`` the current UTC date is used.
    """
    if date is None:
        date = datetime.datetime.utcnow().date()
    return _select_quote_for_date(date)


def _print_usage() -> None:
    prog = sys.argv[0]
    print(f"Usage: {prog} [YYYY-MM-DD]\nPrint a motivational quote for today or the supplied date.")


def _cli() -> None:
    if len(sys.argv) > 2:
        _print_usage()
        sys.exit(1)
    if len(sys.argv) == 2:
        try:
            target_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Error: date must be in YYYY-MM-DD format.")
            sys.exit(1)
    else:
        target_date = None
    quote = get_motivation(target_date)
    print(quote)


if __name__ == "__main__":
    _cli()
