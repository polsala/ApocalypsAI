import datetime
from typing import List

# Mock rationale: a static list of whimsical survival tips.
TIPS: List[str] = [
    "Carry a spare rubber duck – you never know when you’ll need a morale boost.",
    "Always keep a pocket‑sized notebook; doodling can distract rogue meteors.",
    "Learn to whistle; it’s surprisingly effective at scaring off mutant squirrels.",
    "Store a single sock in your emergency kit – it doubles as a makeshift glove.",
    "Practice the art of the perfect high‑five; it’ll boost team spirit during evacuations.",
    "Keep a spare roll of toilet paper; it’s the ultimate barter item.",
    "Carry a small mirror; reflective surfaces can confuse laser‑eye drones.",
]


def get_tip_for_date(date: datetime.date) -> str:
    """Return a deterministic tip based on the supplied date.

    The algorithm is simple: compute the ordinal of the date and take the
    modulus with the number of tips. This guarantees the same date always
    yields the same tip without any external state.
    """
    index = date.toordinal() % len(TIPS)
    return TIPS[index]


def main() -> None:
    """CLI entry point – prints today’s tip to stdout."""
    today = datetime.date.today()
    tip = get_tip_for_date(today)
    print(tip)


if __name__ == "__main__":
    main()
