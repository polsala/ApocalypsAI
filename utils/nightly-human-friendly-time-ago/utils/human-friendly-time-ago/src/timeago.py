import datetime
from typing import Union, Optional

# Mock rationale: No external network calls; pure stdlib.

_EMOJI_MAP = {
    "just_now": "⚡",
    "seconds": "⏱",
    "minutes": "⏳",
    "hours": "⏰",
    "yesterday": "🌅",
    "days": "📅",
    "date": "📆",
}


def _parse_timestamp(ts: Union[datetime.datetime, str]) -> datetime.datetime:
    """Return a UTC ``datetime`` from ``ts``.

    * If ``ts`` is a ``datetime`` it is returned (converted to UTC if tz‑aware).
    * If ``ts`` is a string we attempt ``datetime.fromisoformat``; fallback to ``strptime`` for common formats.
    """
    if isinstance(ts, datetime.datetime):
        if ts.tzinfo is not None:
            return ts.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return ts
    # Assume ISO‑8601 string
    try:
        dt = datetime.datetime.fromisoformat(ts)
    except ValueError:
        # Simple fallback for "YYYY‑MM‑DD HH:MM:SS"
        dt = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    if dt.tzinfo is not None:
        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt


def time_ago(
    ts: Union[datetime.datetime, str],
    *,
    now: Optional[datetime.datetime] = None,
    emoji: bool = True,
) -> str:
    """Return a human‑friendly relative time string.

    Parameters
    ----------
    ts:
        Timestamp to describe.
    now:
        Reference point (UTC). If ``None`` uses ``datetime.datetime.utcnow()``.
    emoji:
        Append an emoji when ``True``.
    """
    target = _parse_timestamp(ts)
    ref = now if now is not None else datetime.datetime.utcnow()
    # Ensure both are naive UTC
    if target.tzinfo is not None:
        target = target.replace(tzinfo=None)
    if ref.tzinfo is not None:
        ref = ref.replace(tzinfo=None)

    delta = ref - target
    seconds = int(delta.total_seconds())
    if seconds < 0:
        # Future timestamps – treat as "just now"
        seconds = 0

    # Determine appropriate bucket
    if seconds < 10:
        text = "just now"
        em = _EMOJI_MAP["just_now"]
    elif seconds < 60:
        text = f"{seconds}s ago"
        em = _EMOJI_MAP["seconds"]
    elif seconds < 3600:
        mins = seconds // 60
        text = f"{mins}\u202Fmin ago"  # thin space for readability
        em = _EMOJI_MAP["minutes"]
    elif seconds < 86400:
        hrs = seconds // 3600
        text = f"{hrs}\u202Fh ago"
        em = _EMOJI_MAP["hours"]
    else:
        days = seconds // 86400
        if days == 1:
            text = "yesterday"
            em = _EMOJI_MAP["yesterday"]
        elif days < 7:
            text = f"{days}\u202Fdays ago"
            em = _EMOJI_MAP["days"]
        else:
            # Show calendar date
            text = f"on {target:%b\u202F%d,\u202F%Y}"  # e.g., on Jan 02, 2023
            em = _EMOJI_MAP["date"]

    return f"{text} {em}" if emoji else text
