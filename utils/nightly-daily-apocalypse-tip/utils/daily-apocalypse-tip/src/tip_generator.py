import argparse
import datetime
import sys
from typing import List

# ---------------------------------------------------------------------------
# Tip data – feel free to expand!
# ---------------------------------------------------------------------------
TIPS: List[str] = [
    "Always keep a spare can of beans in your bunker – protein is priceless.",
    "Water is life: store at least one gallon per person per day.",
    "Learn to start a fire without matches – friction, mirrors, or batteries work.",
    "A good night’s sleep improves decision‑making in chaotic scenarios.",
    "Know your exits: map out multiple evacuation routes before you need them.",
    "Radio silence can be golden – listen before you speak.",
    "Never underestimate the power of a well‑timed joke to boost morale.",
    "Solar chargers keep your devices alive when the grid goes dark.",
    "A sturdy pair of boots can save you from a thousand blisters.",
    "Remember: the best defense is a well‑stocked pantry."
]


def _select_tip_for_date(target_date: datetime.date) -> str:
    """Return a tip deterministically based on *target_date*.

    The algorithm uses the date's ordinal (days since 0001‑01‑01) and
    takes the modulus with the number of tips. This guarantees the same
    date always maps to the same tip without any external state.
    """
    index = target_date.toordinal() % len(TIPS)
    return TIPS[index]


def get_tip(target_date: datetime.date | None = None) -> str:
    """Public API – get the tip for *target_date* (defaults to today)."""
    if target_date is None:
        target_date = datetime.date.today()
    return _select_tip_for_date(target_date)


def _parse_cli_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a deterministic daily apocalypse survival tip."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Optional date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_cli_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Error: Invalid date format – {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.date.today()

    tip = get_tip(target_date)
    print(tip)


if __name__ == "__main__":
    main()
