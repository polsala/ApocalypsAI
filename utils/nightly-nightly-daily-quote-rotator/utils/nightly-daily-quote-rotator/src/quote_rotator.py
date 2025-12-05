"""quote_rotator.py

A tiny, self‑contained utility that returns a deterministic quote based on the date.

The algorithm is simple:
    1. Load a static list of quotes.
    2. Convert the target date to an ordinal (days since year 1).
    3. Use ``ordinal % len(quotes)`` to pick a quote.

Because the list is static and the calculation is pure, the output is fully deterministic
and requires **no network access**.
"""

from __future__ import annotations

import argparse
import datetime
from typing import List

# ---------------------------------------------------------------------------
# Static quote bank – feel free to extend!
# ---------------------------------------------------------------------------
_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade… then find someone whose life gave them vodka.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "To err is human; to really mess things up you need a computer.",
    "I would tell you a UDP joke, but you might not get it.",
    "Debugging: Removing the needles from the haystack.",
    "There are 10 types of people: those who understand binary and those who don’t.",
    "In a world full of APIs, be a RESTful endpoint.",
]


def get_quote(target_date: datetime.date | None = None) -> str:
    """Return the quote for *target_date*.

    If *target_date* is ``None`` the function uses ``datetime.date.today()``.
    The selection is deterministic: ``ordinal % len(_QUOTES)``.
    """
    if target_date is None:
        # Mock rationale: we isolate date acquisition for testability.
        target_date = datetime.date.today()
    index = target_date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic daily quote.")
    parser.add_argument(
        "--date",
        type=str,
        help="Optional date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = _parse_args(argv)
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}. Use YYYY-MM-DD.") from exc
    else:
        target_date = None
    quote = get_quote(target_date)
    print(quote)


if __name__ == "__main__":
    main()
