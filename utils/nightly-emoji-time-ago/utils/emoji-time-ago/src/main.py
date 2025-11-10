import sys
import datetime
from typing import Optional

_EMOJI_MAP = [
    (datetime.timedelta(seconds=45), "⏱️"),          # seconds
    (datetime.timedelta(minutes=1), "🕐"),          # minutes
    (datetime.timedelta(hours=1), "🕑"),            # hours
    (datetime.timedelta(days=1), "📅"),            # days
    (datetime.timedelta(weeks=1), "📆"),           # weeks
    (datetime.timedelta(days=30), "📅"),           # months (approx)
    (datetime.timedelta(days=365), "🎉"),          # years (approx)
]

def _parse_iso(timestamp: str) -> datetime.datetime:
    """Parse an ISO‑8601 timestamp (with optional trailing 'Z')."""
    ts = timestamp.rstrip("Z")
    # datetime.fromisoformat handles the offset if present; we force UTC
    dt = datetime.datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)
    return dt.replace(tzinfo=None)  # work in naive UTC for simplicity

def time_ago(timestamp: str, now: Optional[datetime.datetime] = None) -> str:
    """Return a human‑readable relative time string with an emoji.

    Args:
        timestamp: ISO‑8601 string (e.g., "2023-01-01T12:00:00Z").
        now: Optional current time (UTC naive). If omitted, uses ``datetime.datetime.utcnow()``.
    """
    target = _parse_iso(timestamp)
    now = now or datetime.datetime.utcnow()
    delta = now - target
    # Future timestamps are treated as "just now"
    if delta.total_seconds() < 0:
        delta = datetime.timedelta(seconds=0)

    # Determine appropriate unit & emoji
    for limit, emoji in _EMOJI_MAP:
        if delta < limit:
            # Use the previous limit's unit for display
            break
    else:
        # Larger than any defined limit → years
        limit, emoji = _EMOJI_MAP[-1]

    # Compute quantity based on the chosen unit
    if limit == datetime.timedelta(seconds=45):
        qty = int(delta.total_seconds())
        unit = "second" if qty == 1 else "seconds"
    elif limit == datetime.timedelta(minutes=1):
        qty = int(delta.total_seconds() // 60)
        unit = "minute" if qty == 1 else "minutes"
    elif limit == datetime.timedelta(hours=1):
        qty = int(delta.total_seconds() // 3600)
        unit = "hour" if qty == 1 else "hours"
    elif limit == datetime.timedelta(days=1):
        qty = int(delta.total_seconds() // 86400)
        unit = "day" if qty == 1 else "days"
    elif limit == datetime.timedelta(weeks=1):
        qty = int(delta.total_seconds() // (86400 * 7))
        unit = "week" if qty == 1 else "weeks"
    elif limit == datetime.timedelta(days=30):
        qty = int(delta.total_seconds() // (86400 * 30))
        unit = "month" if qty == 1 else "months"
    else:
        qty = int(delta.total_seconds() // (86400 * 365))
        unit = "year" if qty == 1 else "years"

    # Guard against zero quantity (e.g., just now)
    if qty == 0:
        return f"⏱️ just now"
    return f"{emoji} {qty} {unit} ago"

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji-time-ago.src.main <ISO‑timestamp>")
        sys.exit(2)
    ts = sys.argv[1]
    print(time_ago(ts))

if __name__ == "__main__":
    _cli()
