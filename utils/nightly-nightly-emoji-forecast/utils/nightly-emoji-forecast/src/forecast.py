#!/usr/bin/env python3
"""
emoji forecast utility
"""

import sys
from typing import List


def get_emoji_forecast(temp_c: float) -> str:
    """Return an emoji representing the weather for the given temperature in Celsius."""
    if temp_c <= 0:
        return "🥶"
    if 0 < temp_c <= 10:
        return "🌨️"
    if 10 < temp_c <= 20:
        return "🌤️"
    if 20 < temp_c <= 30:
        return "☀️"
    return "🔥"


def main(argv: List[str] | None = None) -> int:
    """CLI entry point."""
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m src.forecast <temperature>", file=sys.stderr)
        return 2
    try:
        temp = float(argv[0])
    except ValueError:
        print(f"Invalid temperature: {argv[0]}", file=sys.stderr)
        return 1
    print(get_emoji_forecast(temp))
    return 0


if __name__ == "__main__":
    sys.exit(main())
