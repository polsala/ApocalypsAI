import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def convert_time(timestamp: str, from_tz: str, to_tz: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Convert *timestamp* from *from_tz* to *to_tz*.

    Args:
        timestamp: Input datetime string.
        from_tz: Source IANA time zone name.
        to_tz: Target IANA time zone name.
        fmt: Format used for both parsing and output (default ``"%Y-%m-%d %H:%M:%S"``).

    Returns:
        The converted datetime string formatted with *fmt*.
    """
    # Parse the naive datetime according to the provided format
    naive_dt = datetime.strptime(timestamp, fmt)
    # Localize to the source timezone
    src_dt = naive_dt.replace(tzinfo=ZoneInfo(from_tz))
    # Convert to target timezone
    tgt_dt = src_dt.astimezone(ZoneInfo(to_tz))
    return tgt_dt.strftime(fmt)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert timestamps between IANA time zones.")
    parser.add_argument("--time", required=True, help="Input timestamp string.")
    parser.add_argument("--from", dest="from_tz", required=True, help="Source IANA time zone.")
    parser.add_argument("--to", dest="to_tz", required=True, help="Target IANA time zone.")
    parser.add_argument(
        "--format",
        default="%Y-%m-%d %H:%M:%S",
        help="Datetime format for parsing and output (default: %%Y-%%m-%%d %%H:%%M:%%S).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = convert_time(args.time, args.from_tz, args.to_tz, args.format)
        print(result)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
