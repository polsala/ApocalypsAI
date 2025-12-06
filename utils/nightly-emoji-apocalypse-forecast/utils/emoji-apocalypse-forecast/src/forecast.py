"""emoji_apocalypse_forecast
================================
A tiny, self‑contained utility that maps an ISO‑date string to an apocalypse‑themed emoji.

The mapping is deterministic and offline – it simply sums the Unicode code points of the
input string, takes the remainder modulo the number of emojis, and returns the corresponding
emoji.

The module also provides a small CLI for convenience.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# 🎭 The ten whimsical apocalypse emojis we rotate through.
_EMOJIS: List[str] = [
    "🌞",  # Sun – calm before the storm
    "🌧️",  # Rain – ominous clouds
    "🌩️",  # Lightning – sudden danger
    "🌪️",  # Tornado – chaos
    "☄️",  # Comet – celestial threat
    "🌋",  # Volcano – eruption
    "💥",  # Explosion – impact
    "🧨",  # Firecracker – surprise
    "🪐",  # Ringed planet – alien omen
    "🌌",  # Milky Way – cosmic mystery
]


def _checksum(date_str: str) -> int:
    """Return a simple checksum of *date_str*.

    The checksum is the sum of the Unicode code points of the characters in the string.
    This keeps the implementation lightweight and fully deterministic.
    """
    return sum(ord(ch) for ch in date_str)


def forecast(date_str: str | None = None) -> str:
    """Return an apocalypse emoji for *date_str*.

    Parameters
    ----------
    date_str:
        An ISO‑8601 date (``YYYY-MM-DD``). If ``None`` the current local date is used.

    Returns
    -------
    str
        One of the emojis from ``_EMOJIS``.

    Raises
    ------
    ValueError
        If *date_str* is provided but is not a valid ISO‑8601 date.
    """
    if date_str is None:
        date_obj = datetime.date.today()
        date_str = date_obj.isoformat()
    else:
        # Validate the format – ``datetime.date.fromisoformat`` raises ``ValueError`` on failure.
        try:
            datetime.date.fromisoformat(date_str)
        except Exception as exc:
            raise ValueError(f"Invalid ISO‑date string: {date_str!r}") from exc

    idx = _checksum(date_str) % len(_EMOJIS)
    return _EMOJIS[idx]


def _cli() -> None:
    """Entry‑point for ``python -m utils.emoji-apocalypse-forecast.src.forecast``.

    Usage
    -----
    ``python -m utils.emoji-apocalypse-forecast.src.forecast [DATE]``
    If *DATE* is omitted, today's date is used.
    """
    if len(sys.argv) > 2:
        print("Usage: python -m utils.emoji-apocalypse-forecast.src.forecast [ISO_DATE]", file=sys.stderr)
        sys.exit(1)
    date_arg = sys.argv[1] if len(sys.argv) == 2 else None
    try:
        emoji = forecast(date_arg)
        print(emoji)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
