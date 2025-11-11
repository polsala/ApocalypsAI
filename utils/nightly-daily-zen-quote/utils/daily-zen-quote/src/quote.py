import datetime
import random
import sys

# Mock rationale: a small, self‑contained list of inspirational quotes.
QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
]

def _pick_quote_for_date(date: datetime.date) -> str:
    """Return a deterministic quote for *date*.

    The function seeds a ``random.Random`` instance with ``date.toordinal()``
    and selects a quote via ``choice``. Using a local ``Random`` instance
    guarantees that the global random state is untouched.
    """
    rng = random.Random(date.toordinal())
    return rng.choice(QUOTES)

def get_today_quote() -> str:
    """Public API – returns today's zen quote.

    This wrapper exists so that the CLI and tests can call a single entry
    point without needing to pass a date.
    """
    today = datetime.date.today()
    return _pick_quote_for_date(today)

def main() -> None:
    """CLI entry point – prints the quote to stdout.
    """
    quote = get_today_quote()
    print(quote)

if __name__ == "__main__":
    # When executed as a module ``python -m daily_zen_quote`` we expose the CLI.
    main()
