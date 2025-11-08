import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a datetime from one IANA time‑zone to another."
    )
    parser.add_argument(
        "--from",
        dest="from_tz",
        required=True,
        help="Source IANA time‑zone (e.g., 'America/New_York')",
    )
    parser.add_argument(
        "--to",
        dest="to_tz",
        required=True,
        help="Target IANA time‑zone (e.g., 'Asia/Tokyo')",
    )
    parser.add_argument(
        "--time",
        dest="time_str",
        required=True,
        help="Datetime in 'YYYY-MM-DD HH:MM' format",
    )
    return parser.parse_args(argv)


def convert_time(time_str: str, from_tz: str, to_tz: str) -> str:
    """Convert *time_str* from *from_tz* to *to_tz*.

    Returns a formatted string ``'YYYY-MM-DD HH:MM (TZ)'``.
    Raises ``ValueError`` for malformed inputs.
    """
    try:
        naive_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except Exception as exc:
        raise ValueError(f"Invalid time format: {time_str!r}. Expected 'YYYY-MM-DD HH:MM'.") from exc

    try:
        src_zone = ZoneInfo(from_tz)
    except Exception as exc:
        raise ValueError(f"Unknown source time‑zone: {from_tz!r}") from exc

    try:
        tgt_zone = ZoneInfo(to_tz)
    except Exception as exc:
        raise ValueError(f"Unknown target time‑zone: {to_tz!r}") from exc

    # Attach source zone (aware datetime)
    aware_src = naive_dt.replace(tzinfo=src_zone)
    # Convert
    aware_tgt = aware_src.astimezone(tgt_zone)
    return aware_tgt.strftime("%Y-%m-%d %H:%M") + f" ({to_tz})"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = convert_time(args.time_str, args.from_tz, args.to_tz)
        print(result)
        return 0
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
