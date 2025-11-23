from __future__ import annotations

from datetime import datetime, timezone, timedelta


def format_relative(target: datetime, reference: datetime | None = None) -> str:
    """Return a human‑readable relative time string between ``target`` and ``reference``.

    If ``reference`` is omitted, ``datetime.now(timezone.utc)`` is used.
    Examples:
        - "just now"
        - "5 seconds ago"
        - "in 2 minutes"
        - "3 hours ago"
        - "in 1 day"
    """
    if reference is None:
        reference = datetime.now(timezone.utc)
    # Ensure both are timezone‑aware
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)

    delta = target - reference
    seconds = int(delta.total_seconds())
    abs_seconds = abs(seconds)

    if abs_seconds < 5:
        return "just now"

    # Define thresholds for each unit
    intervals = (
        (60, "second", "seconds"),
        (60, "minute", "minutes"),
        (24, "hour", "hours"),
        (7, "day", "days"),
        (4, "week", "weeks"),
        (12, "month", "months"),
        (float("inf"), "year", "years"),
    )

    count = abs_seconds
    unit = "second"
    plural = "seconds"
    for limit, singular, plural_form in intervals:
        if count < limit:
            unit = singular
            plural = plural_form
            break
        count //= limit
        unit = singular
        plural = plural_form

    count = int(round(count))
    word = unit if count == 1 else plural

    if seconds > 0:
        return f"in {count} {word}"
    else:
        return f"{count} {word} ago"
