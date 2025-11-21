import re
import sys
from typing import Final

# ANSI colour codes
RED: Final = "\033[31m"
YELLOW: Final = "\033[33m"
GREEN: Final = "\033[32m"
RESET: Final = "\033[0m"

# Mapping of keyword to colour
_KEYWORD_COLOURS = {
    "error": RED,
    "warning": YELLOW,
    "info": GREEN,
}

def _replace_match(match: re.Match) -> str:
    """Return the coloured replacement for a regex match.

    The match is guaranteed to be one of the keys in ``_KEYWORD_COLOURS``.
    """
    word = match.group(0)
    colour = _KEYWORD_COLOURS[word.lower()]
    return f"{colour}{word}{RESET}"

def colorize(text: str) -> str:
    """Return *text* with ``error``, ``warning`` and ``info`` highlighted.

    The replacement is case‑insensitive and preserves the original case of the
    matched word.
    """
    pattern = re.compile(r"(?i)\b(error|warning|info)\b")
    return pattern.sub(_replace_match, text)

def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m utils.nightly-ansi-colorizer.src.colorizer "Your message"``
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-ansi-colorizer.src.colorizer \"message\"")
        sys.exit(1)
    message = sys.argv[1]
    print(colorize(message))

if __name__ == "__main__":
    _cli()
