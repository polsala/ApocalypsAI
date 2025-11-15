import datetime

# List of Zen quotes. Feel free to add more!
QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "Be present, not perfect.",
    "Simplicity is the ultimate sophistication."
]


def _date_index(date: datetime.date) -> int:
    """Convert a date to a deterministic index within QUOTES.

    The algorithm is deliberately simple: sum of year, month, and day modulo
    the number of quotes. This yields a repeatable quote for any given date.
    """
    return (date.year + date.month + date.day) % len(QUOTES)


def get_today_quote() -> str:
    """Return the Zen quote for *today* based on the deterministic algorithm.

    Returns:
        str: The selected quote.
    """
    today = datetime.date.today()
    idx = _date_index(today)
    return QUOTES[idx]


if __name__ == "__main__":
    print(get_today_quote())
