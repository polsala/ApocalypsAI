import datetime
import sys

# A short, whimsical collection of quotes.
QUOTES = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I intend to live forever. So far, so good.",
    "If at first you don’t succeed, skydiving is not for you.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
]


def get_quote(target_date: datetime.date | None = None) -> str:
    """Return the quote for *target_date*.

    If *target_date* is ``None`` the current local date is used.
    The selection is deterministic: ``(day_of_year - 1) % len(QUOTES)``.
    """
    if target_date is None:
        target_date = datetime.date.today()
    day_of_year = target_date.timetuple().tm_yday
    index = (day_of_year - 1) % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    """CLI entry point – prints the quote for today to stdout."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument for quick manual testing: ``python -m src.quote 2023-01-01``
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_quote(custom_date))
    else:
        main()
