import os
import sys
import datetime

EMOJIS = [
    "\uD83D\uDD1B",  # 🕛 0 or 12
    "\uD83D\uDD50",  # 🕐 1
    "\uD83D\uDD51",  # 🕑 2
    "\uD83D\uDD52",  # 🕒 3
    "\uD83D\uDD53",  # 🕓 4
    "\uD83D\uDD54",  # 🕔 5
    "\uD83D\uDD55",  # 🕕 6
    "\uD83D\uDD56",  # 🕖 7
    "\uD83D\uDD57",  # 🕗 8
    "\uD83D\uDD58",  # 🕘 9
    "\uD83D\uDD59",  # 🕙 10
    "\uD83D\uDD5A",  # 🕚 11
]


def hour_to_emoji(hour: int) -> str:
    """Convert a 0‑23 hour to the corresponding clock emoji (12‑hour face)."""
    hour12 = hour % 12
    return EMOJIS[hour12]


def get_time() -> datetime.datetime:
    """Return a datetime based on the optional TIME env var (HH:MM).
    If TIME is not set, use the current system time.
    Invalid formats cause the program to exit with code 1."""
    time_str = os.getenv("TIME")
    if time_str:
        try:
            dt = datetime.datetime.strptime(time_str, "%H:%M")
        except ValueError:
            print(f"Invalid TIME format: {time_str}", file=sys.stderr)
            sys.exit(1)
    else:
        dt = datetime.datetime.now()
    return dt


def main() -> None:
    dt = get_time()
    emoji = hour_to_emoji(dt.hour)
    print(emoji)


if __name__ == "__main__":
    main()
