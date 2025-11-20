import datetime
from typing import Union


def _now() -> datetime.datetime:
    """Wrapper around ``datetime.datetime.now`` to ease testing.

    The function is deliberately isolated so that unit tests can monkey‑patch
    it without touching the standard library directly.
    """
    return datetime.datetime.now(datetime.timezone.utc)


def _to_datetime(ts: Union[datetime.datetime, int, float]) -> datetime.datetime:
    """Convert a timestamp or ``datetime`` to a UTC ``datetime``.

    * If ``ts`` is a ``datetime`` it is returned as‑is (converted to UTC if it
      has a tzinfo).
    * If ``ts`` is an ``int``/``float`` it is interpreted as a UNIX epoch
      seconds value.
    """
    if isinstance(ts, datetime.datetime):
        if ts.tzinfo is None:
            # Assume naive datetimes are in UTC for simplicity.
            return ts.replace(tzinfo=datetime.timezone.utc)
        return ts.astimezone(datetime.timezone.utc)
    # Assume epoch seconds
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)


def time_ago(ts: Union[datetime.datetime, int, float]) -> str:
    """Return a human‑readable relative time string for *ts*.

    The algorithm is intentionally simple and covers the most common cases.
    It mirrors the style of many social‑media platforms.
    """
    now = _now()
    target = _to_datetime(ts)
    delta = now - target

    # Future timestamps are treated as "just now"
    if delta.total_seconds() < 0:
        return "just now"

    seconds = int(delta.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7
    months = days // 30
    years = days // 365

    if seconds < 10:
        return "just now"
    if seconds < 60:
        return f"{seconds} seconds ago"
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    if days == 1:
        return "yesterday"
    if days < 7:
        return f"{days} days ago"
    if weeks == 1:
        return "last week"
    if weeks < 4:
        return f"{weeks} weeks ago"
    if months == 1:
        return "last month"
    if months < 12:
        return f"{months} months ago"
    if years == 1:
        return "last year"
    return f"{years} years ago"
