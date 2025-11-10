"""emoji_relative_time
=====================

Utility to format a past ``datetime`` as a relative‑time string prefixed with an emoji.

The implementation is deliberately simple and uses only the Python standard library.
"""

from __future__ import annotations

import datetime as _dt
from typing import Tuple

# Mapping of time unit thresholds (in seconds) to (emoji, singular, plural)
_TIME_UNITS: Tuple[Tuple[int, str, str, str], ...] = (
    (60, "🕐", "second", "seconds"),          # < 1 minute
    (60 * 60, "🕑", "minute", "minutes"),    # < 1 hour
    (60 * 60 * 24, "🕒", "hour", "hours"),   # < 1 day
    (60 * 60 * 24 * 7, "📅", "day", "days"), # < 1 week
    (60 * 60 * 24 * 30, "📆", "week", "weeks"), # < 1 month (approx)
    (60 * 60 * 24 * 365, "🌙", "month", "months"), # < 1 year (approx)
    (float("inf"), "🎉", "year", "years"),   # >= 1 year
)

def _choose_unit(delta_seconds: float) -> Tuple[str, int, str]:
    """Select the appropriate time unit for *delta_seconds*.

    Returns a tuple ``(emoji, count, unit_name)`` where *unit_name* is already
    pluralised if *count* != 1.
    """
    for threshold, emoji, singular, plural in _TIME_UNITS:
        if delta_seconds < threshold:
            # Compute the count in the *previous* unit's scale
            # For the first bucket (seconds) we keep the raw seconds.
            if threshold == 60:
                count = int(delta_seconds)
            else:
                # Determine the divisor for the previous bucket
                prev_threshold = _TIME_UNITS[_TIME_UNITS.index((threshold, emoji, singular, plural)) - 1][0]
                count = int(delta_seconds // prev_threshold)
            unit_name = singular if count == 1 else plural
            return emoji, count, unit_name
    # Fallback – should never hit because of ``inf``
    return "🎉", 0, "years"


def format_relative_time(past: _dt.datetime, now: _dt.datetime | None = None) -> str:
    """Return a human‑readable relative‑time string with an emoji.

    Parameters
    ----------
    past:
        The datetime in the past to compare against ``now``.
    now:
        Reference datetime. If ``None`` (default) uses ``datetime.now()``.

    Returns
    -------
    str
        A string like ``"🕑 5 minutes ago"``.
    """
    if now is None:
        now = _dt.datetime.now(tz=past.tzinfo)
    if past > now:
        raise ValueError("`past` must be earlier than `now`")

    delta = now - past
    delta_seconds = delta.total_seconds()
    emoji, count, unit = _choose_unit(delta_seconds)
    return f"{emoji} {count} {unit} ago"

# Example usage (executed when run as a script)
if __name__ == "__main__":
    example_past = _dt.datetime.now() - _dt.timedelta(minutes=5, seconds=30)
    print(format_relative_time(example_past))
