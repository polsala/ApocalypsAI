import datetime
import sys
from typing import List

# Mock rationale: The list of quotes is static and small, ensuring the utility remains self‑contained.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength.",
]


def get_quote(target_date: datetime.date | None = None) -> str:
    """Return the Zen quote for *target_date*.

    If *target_date* is ``None`` the current local date is used.
    The selection is deterministic: it depends only on the day‑of‑year.
    """
    if target_date is None:
        target_date = datetime.date.today()
    # Day of year is 1‑366 (leap years). Subtract 1 to make it zero‑based.
    day_of_year = target_date.timetuple().tm_yday
    index = (day_of_year - 1) % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument in ISO format for quick manual testing.
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_quote(custom_date))
    else:
        main()
