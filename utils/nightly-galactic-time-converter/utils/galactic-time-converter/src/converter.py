import argparse
import datetime
import sys

# Fixed offset that defines the Galactic epoch (1,000,000 seconds after Unix epoch)
GALACTIC_OFFSET = 1_000_000


def unix_to_galactic(ts: int) -> str:
    """Convert a Unix timestamp to Galactic Standard Time (GT).

    GT format: ``GT-YYYYMMDD-HHMMSS``
    """
    if ts < 0:
        raise ValueError("Unix timestamp must be non‑negative")
    galactic_ts = ts + GALACTIC_OFFSET
    dt = datetime.datetime.utcfromtimestamp(galactic_ts)
    return f"GT-{dt:%Y%m%d-%H%M%S}"


def galactic_to_unix(gt: str) -> int:
    """Convert a Galactic Standard Time string back to a Unix timestamp.

    Raises ``ValueError`` if the format is invalid.
    """
    if not gt.startswith("GT-"):
        raise ValueError("Invalid Galactic Time format: missing 'GT-'")
    try:
        # Split into date and time components
        date_part, time_part = gt[3:].split("-")
        dt = datetime.datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
    except Exception as e:
        raise ValueError("Invalid Galactic Time format") from e
    galactic_ts = int(dt.timestamp())
    return galactic_ts - GALACTIC_OFFSET


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert between Unix timestamp and Galactic Time.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-gt", type=int, help="Unix timestamp to convert to Galactic Time")
    group.add_argument("--to-unix", type=str, help="Galactic Time string to convert to Unix timestamp")
    args = parser.parse_args()

    if args.to_gt is not None:
        try:
            print(unix_to_galactic(args.to_gt))
        except ValueError as e:
            sys.exit(str(e))
    else:
        try:
            print(galactic_to_unix(args.to_unix))
        except ValueError as e:
            sys.exit(str(e))


if __name__ == "__main__":
    main()
