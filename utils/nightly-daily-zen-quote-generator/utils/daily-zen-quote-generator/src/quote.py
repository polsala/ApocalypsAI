import datetime
from typing import List

# A curated list of Zen sayings – feel free to extend.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is pure, joy follows like a shadow that never leaves.",
    "Sitting quietly, doing nothing, spring comes, and the grass grows by itself.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "To know the road ahead, ask those who have traveled it.",
    "The quieter you become, the more you can hear.",
    "A single moment can change a lifetime.",
    "Do not seek the truth; simply stop thinking about it.",
]


def get_daily_zen_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The quote is selected by the day‑of‑year modulo the number of quotes.
    """
    if date is None:
        date = datetime.date.today()
    # ``tm_yday`` is 1‑based; subtract 1 for zero‑based indexing.
    index = (date.timetuple().tm_yday - 1) % len(QUOTES)
    return QUOTES[index]


def main() -> None:
    """CLI entry point – prints today's Zen quote to stdout."""
    print(get_daily_zen_quote())


if __name__ == "__main__":
    main()
