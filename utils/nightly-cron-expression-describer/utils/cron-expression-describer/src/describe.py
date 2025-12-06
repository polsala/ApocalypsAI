"""cron-expression-describer/src/describe.py

Utility to translate a 5‑field cron expression into a human‑readable description.

Supported features:
- `*` meaning "every".
- Single numeric values for each field.
- Weekday lists (e.g., `1,3,5`).

Limitations:
- No ranges, step values, or names (e.g., `JAN`).
- Only standard 5‑field cron (minute hour day month weekday).
"""

from __future__ import annotations

import sys
from typing import List

WEEKDAY_MAP = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday",  # both 0 and 7 are Sunday in cron
}

MONTH_MAP = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

def _parse_field(field: str, name: str) -> str:
    """Return a textual representation for a single cron field.

    Args:
        field: The raw field string from the cron expression.
        name: One of "minute", "hour", "day", "month", "weekday".
    """
    if field == "*":
        return f"every {name}" if name != "weekday" else "every weekday"
    # Handle comma‑separated list of numbers
    parts = field.split(",")
    if name == "weekday":
        names = [WEEKDAY_MAP.get(p, f"day{p}") for p in parts]
        return ", ".join(names)
    if name == "month":
        names = [MONTH_MAP.get(p, f"month{p}") for p in parts]
        return ", ".join(names)
    # For minute, hour, day just return numbers joined by commas
    return ", ".join(parts)

def describe_cron(cron_expr: str) -> str:
    """Convert a 5‑field cron expression into a readable sentence.

    Example:
        >>> describe_cron("30 * 15 * 1,3,5")
        'At minute 30, every hour, on day 15 of every month, on weekdays Monday, Wednesday, Friday.'
    """
    fields = cron_expr.strip().split()
    if len(fields) != 5:
        raise ValueError("Cron expression must have exactly 5 fields (minute hour day month weekday)")
    minute, hour, day, month, weekday = fields

    minute_txt = f"minute {minute}" if minute != "*" else "every minute"
    hour_txt = f"hour {hour}" if hour != "*" else "every hour"
    day_txt = f"day {day}" if day != "*" else "every day"
    month_txt = f"month {month}" if month != "*" else "every month"
    weekday_txt = _parse_field(weekday, "weekday")

    # Build sentence parts
    parts: List[str] = []
    parts.append(f"At {minute_txt}")
    parts.append(f"{hour_txt}")
    if day != "*":
        parts.append(f"on day {day}")
    else:
        parts.append("every day")
    if month != "*":
        parts.append(f"of {MONTH_MAP.get(month, month)}")
    else:
        parts.append("of every month")
    if weekday != "*":
        parts.append(f"on weekdays {weekday_txt}")
    else:
        parts.append("on every weekday")

    # Join with commas and ensure final period
    sentence = ", ".join(parts) + "."
    # Clean up duplicate words (e.g., "every day of every month")
    sentence = sentence.replace("every day of every month", "every day of every month")
    return sentence

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.cron-expression-describer.src.describe \"<cron_expr>\"")
        sys.exit(1)
    expr = sys.argv[1]
    try:
        print(describe_cron(expr))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
