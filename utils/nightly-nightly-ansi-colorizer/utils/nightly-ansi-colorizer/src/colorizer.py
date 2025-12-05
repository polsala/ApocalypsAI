"""ansi_colorizer/src/colorizer.py

Utility for applying ANSI escape codes to strings.

Provides:
- `STYLE_CODES`: mapping of style names to their numeric codes.
- `colorize(text: str, *styles: str) -> str`: returns the text wrapped in the requested ANSI codes.
- Simple CLI entry point for quick ad‑hoc usage.
"""

from __future__ import annotations

import sys
from typing import Iterable, List

# Mapping of style names to ANSI codes (foreground colors and attributes)
STYLE_CODES = {
    # Foreground colors
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    # Bright foreground colors
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
    # Text attributes
    "bold": 1,
    "dim": 2,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "hidden": 8,
}

RESET_CODE = "\x1b[0m"


def _resolve_codes(styles: Iterable[str]) -> List[int]:
    """Convert style names to their numeric ANSI codes.

    Unknown style names are ignored with a warning printed to stderr.
    """
    codes: List[int] = []
    for style in styles:
        code = STYLE_CODES.get(style.lower())
        if code is None:
            print(f"[ansi_colorizer] Warning: unknown style '{style}' ignored", file=sys.stderr)
            continue
        codes.append(code)
    return codes


def colorize(text: str, *styles: str) -> str:
    """Wrap *text* with ANSI escape codes for the given *styles*.

    Parameters
    ----------
    text: str
        The string to be styled.
    *styles: str
        One or more style identifiers (e.g., "red", "bold").

    Returns
    -------
    str
        The styled string, ready for terminal output.
    """
    if not styles:
        return text
    codes = _resolve_codes(styles)
    if not codes:
        return text
    prefix = f"\x1b[{';'.join(str(c) for c in codes)}m"
    return f"{prefix}{text}{RESET_CODE}"


def _cli() -> None:
    """Command‑line interface.

    Usage: python -m ansi_colorizer "text" style1 style2 ...
    """
    if len(sys.argv) < 2:
        print("Usage: python -m ansi_colorizer \"text\" [style ...]", file=sys.stderr)
        sys.exit(1)
    text = sys.argv[1]
    styles = sys.argv[2:]
    print(colorize(text, *styles))


if __name__ == "__main__":
    _cli()
