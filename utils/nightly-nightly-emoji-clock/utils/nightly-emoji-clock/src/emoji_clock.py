"""emoji_clock.py

Utility that converts the current local time into a sequence of clock‑face emojis.

Public API
-----------
- ``get_emoji_time(now: datetime | None = None) -> str``
    Returns a string of one or two emojis representing the hour (and optional half‑hour).
- ``main()``
    CLI entry point that prints the emoji time to stdout.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Optional

# Mapping of hour (1‑12) to clock face emoji
_HOUR_EMOJI = {
    1: "🕐",
    2: "🕑",
    3: "🕒",
    4: "🕓",
    5: "🕔",
    6: "🕕",
    7: "🕖",
    8: "🕗",
    9: "🕘",
    10: "🕙",
    11: "🕚",
    12: "🕛",
}

# Mapping of hour (1‑12) to half‑hour emoji
_HALF_HOUR_EMOJI = {
    1: "🕜",
    2: "🕝",
    3: "🕞",
    4: "🕟",
    5: "🕠",
    6: "🕡",
    7: "🕢",
    8: "🕣",
    9: "🕤",
    10: "🕥",
    11: "🕦",
    12: "🕧",
}


def _hour_to_12h(hour: int) -> int:
    """Convert 0‑23 hour to 12‑hour clock (1‑12)."""
    return ((hour - 1) % 12) + 1


def get_emoji_time(now: Optional[datetime] = None) -> str:
    """Return the current time as clock‑face emoji(s).

    Parameters
    ----------
    now: datetime | None
        Optional datetime to use instead of ``datetime.now()``.  Useful for testing.

    Returns
    -------
    str
        A single emoji for the hour, or hour+half‑hour if minutes ≥ 30.
    """
    now = now or datetime.now()
    hour_12 = _hour_to_12h(now.hour)
    if now.minute >= 30:
        # Use half‑hour emoji
        return _HALF_HOUR_EMOJI[hour_12]
    else:
        return _HOUR_EMOJI[hour_12]


def main() -> None:
    """CLI entry point – prints the emoji time to stdout."""
    emoji = get_emoji_time()
    print(emoji)


if __name__ == "__main__":
    # Allow running as a module: ``python -m nightly_emoji_clock``
    # The module name is derived from the folder name; we expose ``main``.
    main()
