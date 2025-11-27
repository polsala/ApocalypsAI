"""emoji_forecast – deterministic emoji weather generator.

Provides a single public function ``get_forecast`` that returns an emoji string
based on the supplied ``datetime.date``. The algorithm is deliberately simple
and fully deterministic, requiring no external resources.
"""

from __future__ import annotations

import sys
from datetime import date
from typing import List

# List of whimsical weather emojis. The order is fixed to keep the mapping stable.
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌤️",  # partly sunny
    "🌙",  # night
    "🌫️",  # fog
]


def _index_for_date(d: date) -> int:
    """Calculate a stable index into ``EMOJIS`` for the given date.

    The formula is intentionally straightforward: (year + month + day) % len(EMOJIS).
    This yields a repeatable result without any randomness or external state.
    """
    total = d.year + d.month + d.day
    return total % len(EMOJIS)


def get_forecast(d: date) -> str:
    """Return the weather emoji for *d*.

    Parameters
    ----------
    d: datetime.date
        The date for which to compute the forecast.

    Returns
    -------
    str
        An emoji representing the deterministic forecast.
    """
    idx = _index_for_date(d)
    return EMOJIS[idx]


def _parse_cli_arg(arg: str) -> date:
    """Parse a ``YYYY-MM-DD`` string into a ``datetime.date``.

    Raises ``ValueError`` if the format is invalid.
    """
    try:
        year, month, day = map(int, arg.split("-"))
        return date(year, month, day)
    except Exception as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc


def main(argv: list[str] | None = None) -> None:
    """CLI entry point.

    * No arguments – prints today's forecast.
    * One argument – treats it as a ``YYYY-MM-DD`` date.
    """
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        target_date = date.today()
    else:
        target_date = _parse_cli_arg(argv[0])

    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
