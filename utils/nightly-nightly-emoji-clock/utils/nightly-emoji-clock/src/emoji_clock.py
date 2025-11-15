import datetime
from typing import Optional

# Mapping of hour (0‑23) to clock face emojis (12‑hour style)
_HOUR_EMOJIS = {
    0: "🕛",
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
    13: "🕐",
    14: "🕑",
    15: "🕒",
    16: "🕓",
    17: "🕔",
    18: "🕕",
    19: "🕖",
    20: "🕗",
    21: "🕘",
    22: "🕙",
    23: "🕚",
}

# Mapping of minute (0‑59) to half‑hour emojis
_MINUTE_EMOJIS = {
    0: "🕛",
    30: "🕧",
}

def _round_hour(dt: datetime.datetime) -> int:
    """Round to the nearest hour (0‑23)."""
    # If minutes >= 30, round up to next hour
    hour = dt.hour
    if dt.minute >= 30:
        hour = (hour + 1) % 24
    return hour

def _round_minute(dt: datetime.datetime) -> int:
    """Round to the nearest half hour (0 or 30)."""
    return 30 if dt.minute >= 15 else 0

def get_emoji_time(dt: Optional[datetime.datetime] = None) -> str:
    """Return a two‑emoji string representing the hour and minute.

    If *dt* is ``None`` the current UTC time is used.
    """
    if dt is None:
        dt = datetime.datetime.utcnow()
    # Ensure we work with a naive datetime in UTC
    if dt.tzinfo is not None:
        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    hour = _round_hour(dt)
    minute = _round_minute(dt)
    hour_emoji = _HOUR_EMOJIS[hour]
    minute_emoji = _MINUTE_EMOJIS[minute]
    return f"{hour_emoji}{minute_emoji}"

def main() -> None:
    """CLI entry point – prints the emoji clock for the current UTC time."""
    print(get_emoji_time())

if __name__ == "__main__":
    main()
