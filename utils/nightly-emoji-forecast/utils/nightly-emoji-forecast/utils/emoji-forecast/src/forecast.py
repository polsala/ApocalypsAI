"""Emoji Weather Forecast utility.

Generates a deterministic, whimsical weather forecast for a given date,
represented by an emoji and a temperature in Celsius.
"""

from __future__ import annotations
import datetime
from typing import Optional


def _temperature_for_date(date: datetime.date) -> int:
    """Deterministic pseudo‑random temperature between -10 and 40°C.

    The algorithm is deliberately simple and reproducible:
    1. Convert the date to its ordinal.
    2. Multiply by a prime (7) and take modulo 51 (range size).
    3. Shift to start at -10.
    """
    # Mock rationale: deterministic temperature without external RNG.
    ordinal = date.toordinal()
    temp = ((ordinal * 7) % 51) - 10
    return temp


def _emoji_for_temperature(temp: int) -> str:
    """Map temperature to an emoji."""
    if temp < 0:
        return "❄️"
    if temp < 10:
        return "☁️"
    if temp < 20:
        return "🌤️"
    if temp < 30:
        return "☀️"
    return "🔥"


def generate_forecast(date: Optional[datetime.date] = None) -> str:
    """Return a forecast string like "☀️ 22°C".

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    temp = _temperature_for_date(date)
    emoji = _emoji_for_temperature(temp)
    return f"{emoji} {temp}°C"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Emoji weather forecast")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    args = parser.parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        target_date = None
    print(generate_forecast(target_date))
