"""emoji_date_formatter – Convert dates to whimsical emoji strings.

Provides both a library function `format_date` and a tiny CLI.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import Union

# Mapping of month numbers to emojis (feel free to tweak)
_MONTH_EMOJIS = {
    1: "❄️",   # January – snow
    2: "❤️",   # February – love
    3: "🌱",   # March – sprout
    4: "🌸",   # April – blossoms
    5: "🌼",   # May – flowers
    6: "☀️",   # June – sun
    7: "🏖️",   # July – beach
    8: "🍉",   # August – fruit
    9: "🍂",   # September – leaves falling
    10: "🎃",  # October – pumpkin
    11: "🦃",  # November – turkey
    12: "🎄",  # December – Christmas tree
}

_CALENDAR_EMOJI = "📅"


def _ensure_date(value: Union[str, date, datetime]) -> date:
    """Coerce *value* into a :class:`datetime.date`.

    Accepts ISO‑8601 strings (``YYYY-MM-DD``), ``datetime`` objects, or ``date`` objects.
    Raises ``ValueError`` for unsupported formats.
    """
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(f"String '{value}' is not a valid ISO‑8601 date (YYYY-MM-DD).") from exc
    raise TypeError(f"Unsupported type for date conversion: {type(value)!r}")


def format_date(value: Union[str, date, datetime]) -> str:
    """Return an emoji representation of *value*.

    Example
    -------
    >>> format_date('2023-12-25')
    '🎄📅'
    """
    d = _ensure_date(value)
    month_emoji = _MONTH_EMOJIS.get(d.month, "")
    # Day is shown as the number followed by the calendar emoji for readability.
    day_part = f"{d.day}{_CALENDAR_EMOJI}"
    return f"{month_emoji}{day_part}"


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Convert a date to an emoji string.")
    parser.add_argument(
        "date",
        help="Date to format (ISO‑8601, e.g., 2023-12-25).",
    )
    args = parser.parse_args()
    try:
        result = format_date(args.date)
    except Exception as exc:  # pragma: no cover – defensive, not expected in tests
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(result)


if __name__ == "__main__":  # pragma: no cover – exercised via CLI test
    _cli()
