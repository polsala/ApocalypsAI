"""daily_zen_quote_generator – deterministic zen quotes based on date.

Provides:
- `get_zen_quote(date: datetime.date) -> str`
- CLI entry point `python -m daily_zen_quote_generator [YYYY-MM-DD]`
"""

from __future__ import annotations

import sys
from datetime import date, datetime
from typing import List

# Mock rationale: static list ensures offline deterministic behavior.
QUOTES: List[str] = [
    "Be present.",
    "Embrace impermanence.",
    "Flow like water.",
    "Silence speaks.",
    "Know yourself.",
]


def get_zen_quote(target_date: date) -> str:
    """Return a zen quote for *target_date*.

    The quote is selected by taking the day‑of‑year (1‑based), subtracting one,
    and taking the remainder modulo the number of quotes.
    """
    day_of_year = target_date.timetuple().tm_yday
    index = (day_of_year - 1) % len(QUOTES)
    return QUOTES[index]


def _parse_cli_arg(arg: str) -> date:
    """Parse a CLI argument into a :class:`datetime.date`.

    Accepts ISO format ``YYYY-MM-DD``. Raises ``ValueError`` on failure.
    """
    try:
        return datetime.strptime(arg, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc


def main(argv: List[str] | None = None) -> None:
    """CLI entry point.

    * No arguments – prints today's quote.
    * One argument – interpreted as a date in ``YYYY-MM-DD`` format.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        target = date.today()
    elif len(argv) == 1:
        target = _parse_cli_arg(argv[0])
    else:
        print("Usage: python -m daily_zen_quote_generator [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)

    print(get_zen_quote(target))


if __name__ == "__main__":
    main()
