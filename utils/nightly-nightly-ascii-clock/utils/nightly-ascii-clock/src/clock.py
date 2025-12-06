import datetime
import sys

# Mapping of each digit to a 5‑line ASCII representation
_DIGIT_ART = {
    "0": [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    "1": [
        "  █  ",
        " ██  ",
        "  █  ",
        "  █  ",
        " ███ "
    ],
    "2": [
        " ███ ",
        "    █",
        " ███ ",
        "█    ",
        " ███ "
    ],
    "3": [
        " ███ ",
        "    █",
        " ███ ",
        "    █",
        " ███ "
    ],
    "4": [
        "█   █",
        "█   █",
        " ███ ",
        "    █",
        "    █"
    ],
    "5": [
        " ███ ",
        "█    ",
        " ███ ",
        "    █",
        " ███ "
    ],
    "6": [
        " ███ ",
        "█    ",
        " ███ ",
        "█   █",
        " ███ "
    ],
    "7": [
        " ███ ",
        "    █",
        "   █ ",
        "  █  ",
        " █   "
    ],
    "8": [
        " ███ ",
        "█   █",
        " ███ ",
        "█   █",
        " ███ "
    ],
    "9": [
        " ███ ",
        "█   █",
        " ███ ",
        "    █",
        " ███ "
    ],
    ":": [
        "     ",
        "  █  ",
        "     ",
        "  █  ",
        "     "
    ]
}


def get_ascii_time(dt: datetime.datetime) -> str:
    """Return a multi‑line string rendering ``dt`` as HH:MM in ASCII art.

    The function pads single‑digit hours/minutes with a leading zero to keep the layout stable.
    """
    time_str = dt.strftime("%H:%M")
    # Build each of the 5 lines by concatenating the corresponding slice from each character
    lines = ["" for _ in range(5)]
    for ch in time_str:
        art = _DIGIT_ART.get(ch)
        if art is None:
            raise ValueError(f"Unsupported character in time string: {ch}")
        for i, segment in enumerate(art):
            lines[i] += segment + "  "  # two spaces between characters for readability
    return "\n".join(lines)


def _main() -> None:
    now = datetime.datetime.now()
    ascii_clock = get_ascii_time(now)
    print(ascii_clock)


if __name__ == "__main__":
    _main()
