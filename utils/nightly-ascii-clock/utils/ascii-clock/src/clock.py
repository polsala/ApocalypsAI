import datetime
from typing import List

# ASCII representations for digits 0‑9 and colon
_DIGITS = {
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

def _render_char(ch: str) -> List[str]:
    """Return the three‑line ASCII art for a single character.

    Args:
        ch: A character from '0'‑'9' or ':'.
    """
    if ch not in _DIGITS:
        raise ValueError(f"Unsupported character for ASCII clock: {ch!r}")
    return _DIGITS[ch]

def get_ascii_time(dt: datetime.datetime) -> str:
    """Convert a ``datetime`` object to a multi‑line ASCII clock string.

    The time is formatted as ``HH:MM`` using a 24‑hour clock.
    """
    time_str = dt.strftime("%H:%M")
    # Build three lines by concatenating the corresponding slice of each digit
    lines = ["" for _ in range(3)]
    for idx, ch in enumerate(time_str):
        char_art = _render_char(ch)
        for i in range(3):
            # Add a space between characters except before the first one
            if idx > 0:
                lines[i] += " "
            lines[i] += char_art[i]
    return "\n".join(lines)

def render_current_time() -> str:
    """Render *now* as an ASCII clock.

    This helper is used by the CLI entry‑point and the test suite.
    """
    now = datetime.datetime.now()
    return get_ascii_time(now)

if __name__ == "__main__":
    print(render_current_time())
