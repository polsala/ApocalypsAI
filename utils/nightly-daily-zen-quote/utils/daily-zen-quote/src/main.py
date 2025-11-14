import datetime
import sys
from typing import List

# Mock rationale: Hard‑coded list keeps the utility self‑contained and offline.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Know yourself and you will win all battles.",
    "Patience is a virtue, not a weakness.",
    "When the mind is still, the soul speaks.",
    "A single spark can start a great fire.",
    "Harmony arises from balance.",
    "Listen more than you speak."
]


def get_zen_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The quote is selected by ``day_of_year % len(QUOTES)``.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    index = day_of_year % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    quote = get_zen_quote()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument for quick manual testing: YYYY-MM-DD
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
            print(get_zen_quote(custom_date))
        except ValueError:
            sys.stderr.write("Invalid date format. Use YYYY-MM-DD.\n")
            sys.exit(1)
    else:
        main()
