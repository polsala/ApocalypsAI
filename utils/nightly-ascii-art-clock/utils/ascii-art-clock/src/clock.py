import datetime

DIGITS = {
    "0": [" _ ", "| |", "|_|"],
    "1": ["   ", "  |", "  |"],
    "2": [" _ ", " _|", "|_ "],
    "3": [" _ ", " _|", " _|"],
    "4": ["   ", "|_|", "  |"],
    "5": [" _ ", "|_ ", " _|"],
    "6": [" _ ", "|_ ", "|_|"],
    "7": [" _ ", "  |", "  |"],
    "8": [" _ ", "|_|", "|_|"],
    "9": [" _ ", "|_|", " _|"],
    ":": ["   ", " . ", " . "]
}


def render_time(dt: datetime.time) -> str:
    """Return ASCII art representation of given time (HH:MM)."""
    time_str = dt.strftime("%H:%M")
    lines = ["", "", ""]
    for ch in time_str:
        art = DIGITS.get(ch, ["   ", "   ", "   "])
        for i in range(3):
            lines[i] += art[i] + " "
    return "\n".join(line.rstrip() for line in lines)


def main():
    now = datetime.datetime.now().time()
    print(render_time(now))


if __name__ == "__main__":
    main()
