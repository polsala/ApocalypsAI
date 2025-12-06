import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

__all__ = ["convert_time"]


def _parse_datetime(dt_str: str) -> datetime:
    """Parse a datetime string in the expected ``YYYY-MM-DD HH:MM:SS`` format.

    Raises:
        ValueError: If the string does not match the format.
    """
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")


def convert_time(dt_str: str, from_tz: str, to_tz: str) -> str:
    """Convert *dt_str* from *from_tz* to *to_tz* and return an ISO‑8601 string.

    Args:
        dt_str: Datetime string in ``YYYY-MM-DD HH:MM:SS`` format.
        from_tz: IANA time‑zone name of the source timezone.
        to_tz: IANA time‑zone name of the target timezone.

    Returns:
        ISO‑8601 formatted datetime with the target offset, e.g.
        ``2025-01-02 05:30:00+09:00``.
    """
    # Parse naive datetime
    naive_dt = _parse_datetime(dt_str)
    # Attach source timezone
    try:
        source_zone = ZoneInfo(from_tz)
    except Exception as exc:
        raise ValueError(f"Invalid source timezone '{from_tz}': {exc}")
    aware_dt = naive_dt.replace(tzinfo=source_zone)
    # Convert to target timezone
    try:
        target_zone = ZoneInfo(to_tz)
    except Exception as exc:
        raise ValueError(f"Invalid target timezone '{to_tz}': {exc}")
    target_dt = aware_dt.astimezone(target_zone)
    # Return ISO‑8601 without the ``T`` separator for readability
    return target_dt.strftime("%Y-%m-%d %H:%M:%S%z")


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a datetime string between IANA time zones."
    )
    parser.add_argument("datetime", help="Datetime in 'YYYY-MM-DD HH:MM:SS' format")
    parser.add_argument("from_tz", help="Source IANA timezone, e.g., 'America/New_York'")
    parser.add_argument("to_tz", help="Target IANA timezone, e.g., 'Asia/Tokyo'")
    args = parser.parse_args()
    try:
        result = convert_time(args.datetime, args.from_tz, args.to_tz)
        print(result)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
