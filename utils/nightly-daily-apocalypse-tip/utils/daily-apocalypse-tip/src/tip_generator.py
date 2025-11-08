"""Tip generator for daily apocalypse survival.

Provides a deterministic tip based on the given date.
"""

from __future__ import annotations
import argparse
import datetime
from typing import List

_TIPS: List[str] = [
    "Carry a spare pair of socks; they make great fire starters.",
    "Never trust a talking cactus; they're liars.",
    "A well‑timed nap can outlast a meteor shower.",
    "Remember: duct tape fixes everything, even morale.",
    "Keep a rubber duck handy; it doubles as a flotation device.",
    "If you hear a siren, it's probably just the neighbor's karaoke.",
    "Stockpile canned beans; they're the ultimate barter currency.",
    "A good joke can distract a zombie for at least 30 seconds.",
    "Always have a backup plan, and a backup for that backup.",
    "Sunrise is nature's reminder to keep moving."
]


def get_tip(date: datetime.date | None = None) -> str:
    """Return the tip for the given date.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    The selection is deterministic: ``date.toordinal() % len(_TIPS)``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_TIPS)
    return _TIPS[index]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a daily apocalypse survival tip."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Specify a date (YYYY-MM-DD) to get the tip for that day. Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    tip = get_tip(args.date)
    print(f"🛡️  Today's apocalypse tip: {tip}")


if __name__ == "__main__":
    main()
