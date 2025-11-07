#!/usr/bin/env python3
"""time‑ago‑cli

A tiny command‑line tool that converts a timestamp into a human‑readable
relative‑time string (e.g., "5 minutes ago").

Usage:
    python -m utils.time-ago-cli.src.main "2023-08-15T12:34:56" [--emoji]
"""

import argparse
import datetime
import sys
from typing import Union

# ---------------------------------------------------------------------------
# Core logic – pure functions, easy to test
# ---------------------------------------------------------------------------

def _parse_timestamp(ts: str) -> datetime.datetime:
    """Parse *ts* which may be an ISO‑8601 string or a Unix epoch integer.

    Returns a timezone‑aware ``datetime`` in UTC.
    """
    # Mock rationale: we avoid external libraries; datetime.fromisoformat handles most ISO strings.
    try:
        # Try ISO‑8601 first
        dt = datetime.datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        else:
            dt = dt.astimezone(datetime.timezone.utc)
        return dt
    except ValueError:
        # Fallback: treat as epoch seconds (int or float)
        try:
            epoch = float(ts)
            return datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)
        except ValueError as exc:
            raise ValueError(f"Unable to parse timestamp: {ts}") from exc


def _humanize_delta(delta: datetime.timedelta) -> str:
    """Convert a ``timedelta`` into a friendly string.

    The algorithm chooses the largest appropriate unit (seconds, minutes,
    hours, days, months, years) and rounds down.
    """
    seconds = int(delta.total_seconds())
    if seconds < 0:
        return "in the future"
    if seconds < 10:
        return "just now"
    if seconds < 60:
        return f"{seconds} seconds ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    months = days // 30
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = months // 12
    return f"{years} year{'s' if years != 1 else ''} ago"


def _emoji_for_delta(delta: datetime.timedelta) -> str:
    """Select an emoji that roughly matches the age.

    This is purely whimsical; the mapping is deterministic.
    """
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "⏱️"
    if seconds < 3600:
        return "🌱"
    if seconds < 86400:
        return "🌿"
    if seconds < 30 * 86400:
        return "🌳"
    if seconds < 365 * 86400:
        return "🍂"
    return "🪐"


def time_ago(ts: Union[str, datetime.datetime], *, emoji: bool = False) -> str:
    """Public API – return a human‑readable relative time string.

    Parameters
    ----------
    ts:
        Either an ISO‑8601 string, a Unix epoch string/int, or a ``datetime``.
    emoji:
        If ``True``, append a matching emoji.
    """
    if isinstance(ts, datetime.datetime):
        dt = ts
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        else:
            dt = dt.astimezone(datetime.timezone.utc)
    else:
        dt = _parse_timestamp(str(ts))
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - dt
    human = _humanize_delta(delta)
    if emoji:
        human += f" {_emoji_for_delta(delta)}"
    return human


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert a timestamp to a human‑readable 'time ago' string.")
    parser.add_argument("timestamp", help="ISO‑8601 string or Unix epoch seconds (e.g., 2023-08-15T12:34:56 or 1692102896)")
    parser.add_argument("-e", "--emoji", action="store_true", help="Append a whimsical emoji representing the age")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = time_ago(args.timestamp, emoji=args.emoji)
        print(result)
        return 0
    except Exception as exc:  # pragma: no cover – defensive
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
