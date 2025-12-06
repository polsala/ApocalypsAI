"""Doom Level Assessor utility.

Provides a function to compute a doom level based on distance to a fixed
apocalypse date (2099‑12‑31). Also offers a simple CLI.
"""

from __future__ import annotations

import sys
from datetime import datetime, date

APOCALYPSE_DATE = date(2099, 12, 31)


def parse_date(date_str: str) -> date:
    """Parse an ISO date string (YYYY‑MM‑DD) into a :class:`datetime.date`.

    Raises
    ------
    ValueError
        If the string does not match the expected format.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected YYYY-MM-DD.") from exc


def compute_doom_level(date_str: str) -> str:
    """Return a doom level for the given date string.

    Levels
    ------
    * ``"Already passed"`` – the date is after the apocalypse.
    * ``"Safe"``          – more than 10 years remaining.
    * ``"Warning"``       – 2 – 10 years remaining.
    * ``"Critical"``      – 6 months – 2 years remaining.
    * ``"Apocalypse"``    – six months or less remaining.
    """
    target = parse_date(date_str)
    if target > APOCALYPSE_DATE:
        return "Already passed"

    delta_days = (APOCALYPSE_DATE - target).days

    if delta_days > 3650:  # >10 years
        return "Safe"
    if delta_days > 730:   # >2 years
        return "Warning"
    if delta_days > 180:   # >6 months
        return "Critical"
    return "Apocalypse"


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Parameters
    ----------
    argv:
        Optional list of arguments (excluding the program name). If ``None``
        ``sys.argv[1:]`` is used.
    """
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m src.doom <YYYY-MM-DD>", file=sys.stderr)
        return 1
    try:
        level = compute_doom_level(argv[0])
        print(level)
        return 0
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
