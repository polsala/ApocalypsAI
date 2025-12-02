import datetime
from typing import Optional


def _plural(value: int, singular: str, plural: Optional[str] = None) -> str:
    """Return the appropriate singular/plural word for *value*.

    If *plural* is not supplied, ``singular + 's'`` is used.
    """
    word = singular if value == 1 else (plural or f"{singular}s")
    return f"{value} {word}"


def format_relative_time(
    target: datetime.datetime,
    reference: Optional[datetime.datetime] = None,
) -> str:
    """Return a human‑readable relative time string.

    Parameters
    ----------
    target:
        The datetime to describe.
    reference:
        The datetime to compare against. If ``None`` the current UTC time is used.

    Returns
    -------
    str
        A phrase like ``"5 minutes ago"`` or ``"in 2 days"``.
    """
    if reference is None:
        reference = datetime.datetime.utcnow()

    # Ensure both are timezone‑aware or both naive for a fair comparison.
    if target.tzinfo != reference.tzinfo:
        # Simple approach: drop tzinfo (treat as UTC) – the utility is meant for quick scripts.
        target = target.replace(tzinfo=None)
        reference = reference.replace(tzinfo=None)

    delta = target - reference
    seconds = int(delta.total_seconds())
    abs_seconds = abs(seconds)

    # Very recent events
    if abs_seconds < 5:
        return "just now"

    # Define thresholds
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day
    month = 30 * day  # Approximation
    year = 365 * day  # Approximation

    def _choose(value: int, unit: str) -> str:
        phrase = _plural(value, unit)
        return f"{phrase} ago" if seconds < 0 else f"in {phrase}"

    if abs_seconds < minute:
        return _choose(abs_seconds, "second")
    if abs_seconds < hour:
        minutes = abs_seconds // minute
        return _choose(minutes, "minute")
    if abs_seconds < day:
        hours = abs_seconds // hour
        return _choose(hours, "hour")
    if abs_seconds < week:
        days = abs_seconds // day
        return _choose(days, "day")
    if abs_seconds < month:
        weeks = abs_seconds // week
        return _choose(weeks, "week")
    if abs_seconds < year:
        months = abs_seconds // month
        return _choose(months, "month")
    years = abs_seconds // year
    return _choose(years, "year")
