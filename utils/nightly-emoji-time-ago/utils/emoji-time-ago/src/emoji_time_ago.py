import sys
import datetime
from typing import Optional

# Mapping of elapsed thresholds (in seconds) to emojis
_EMOJI_MAP = [
    (60, "⏱️"),               # < 1 minute
    (3600, "🕒"),            # < 1 hour
    (86400, "🌅"),           # < 1 day
    (604800, "📅"),          # < 7 days
    (float('inf'), "📆"),    # >= 7 days
]

def _choose_emoji(seconds: float) -> str:
    """Return the appropriate emoji for *seconds* elapsed."""
    for threshold, emoji in _EMOJI_MAP:
        if seconds < threshold:
            return emoji
    return "❓"

def _human_readable(seconds: float) -> str:
    """Convert *seconds* into a concise "X unit(s) ago" string."""
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 7:
        return f"{int(days)} day{'s' if days != 1 else ''} ago"
    weeks = days // 7
    return f"{int(weeks)} week{'s' if weeks != 1 else ''} ago"

def format_time_ago(timestamp: str, now: Optional[datetime.datetime] = None) -> str:
    """Return a string like "📅 3 days ago" for the given ISO‑8601 *timestamp*.

    Parameters
    ----------
    timestamp: str
        ISO‑8601 formatted datetime (e.g., ``2025-11-13T10:30:00Z``).
    now: datetime, optional
        Reference point for "now". If omitted, ``datetime.datetime.utcnow()`` is used.
    """
    # Parse the timestamp; support both Z‑suffix and offset‑aware strings.
    try:
        # Python 3.11's fromisoformat does not understand trailing 'Z', so replace.
        ts = timestamp.replace("Z", "+00:00")
        dt = datetime.datetime.fromisoformat(ts)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO‑8601 timestamp: {timestamp}") from exc

    if dt.tzinfo is None:
        # Assume UTC if no timezone info provided.
        dt = dt.replace(tzinfo=datetime.timezone.utc)

    now = now or datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    elapsed = (now - dt).total_seconds()
    if elapsed < 0:
        # Future timestamps are treated as "just now".
        elapsed = 0
    emoji = _choose_emoji(elapsed)
    human = _human_readable(elapsed)
    return f"{emoji} {human}" if human != "just now" else f"{emoji} just now"

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_time_ago <ISO‑8601 timestamp>")
        sys.exit(1)
    ts = sys.argv[1]
    try:
        print(format_time_ago(ts))
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    _cli()
