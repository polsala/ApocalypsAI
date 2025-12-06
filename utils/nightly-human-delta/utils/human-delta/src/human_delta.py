import sys
import argparse
from datetime import datetime, timezone
from typing import Tuple


def _parse_iso(ts: str) -> datetime:
    """Parse an ISO‑8601 timestamp.

    Supports both naive and timezone‑aware strings. Naive timestamps are
    interpreted as UTC.
    """
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO‑8601 timestamp: {ts}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _breakdown(delta_seconds: int) -> Tuple[int, int, int, int]:
    """Return days, hours, minutes, seconds from a total‑seconds count."""
    days, rem = divmod(delta_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return days, hours, minutes, seconds


def diff(start: str, end: str) -> str:
    """Return a human‑readable difference between two ISO‑8601 timestamps.

    Parameters
    ----------
    start, end: str
        ISO‑8601 formatted timestamps.

    Returns
    -------
    str
        Human readable description, e.g. ``"2 days, 3 hours, 5 minutes"``.
    """
    start_dt = _parse_iso(start)
    end_dt = _parse_iso(end)
    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt
    total_seconds = int((end_dt - start_dt).total_seconds())
    days, hours, minutes, seconds = _breakdown(total_seconds)
    parts = []
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return ", ".join(parts)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="human-delta",
        description="Print a human‑readable difference between two ISO‑8601 timestamps."
    )
    parser.add_argument("start", help="Start timestamp (ISO‑8601)")
    parser.add_argument("end", help="End timestamp (ISO‑8601)")
    args = parser.parse_args()
    try:
        result = diff(args.start, args.end)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print(result)


if __name__ == "__main__":
    _cli()
