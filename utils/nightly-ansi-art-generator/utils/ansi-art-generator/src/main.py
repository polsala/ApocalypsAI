import argparse
import random
from typing import List

# ANSI color codes for foreground colors (30‑37) and bright variants (90‑97)
ANSI_COLORS: List[str] = [
    "\u001b[31m",  # red
    "\u001b[32m",  # green
    "\u001b[33m",  # yellow
    "\u001b[34m",  # blue
    "\u001b[35m",  # magenta
    "\u001b[36m",  # cyan
    "\u001b[91m",  # bright red
    "\u001b[92m",  # bright green
    "\u001b[93m",  # bright yellow
    "\u001b[94m",  # bright blue
    "\u001b[95m",  # bright magenta
    "\u001b[96m",  # bright cyan
]
RESET = "\u001b[0m"
BLOCK = "█"


def generate_art(width: int = 40, height: int = 10, palette: List[str] = None) -> str:
    """Return a string containing a rectangle of random ANSI‑colored blocks.

    Args:
        width: Number of characters per line.
        height: Number of lines.
        palette: Optional list of ANSI color codes to use. If omitted, the full
            built‑in palette is used.

    Returns:
        A multi‑line string ready to be printed to a terminal.
    """
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive integers")
    palette = palette or ANSI_COLORS
    lines = []
    for _ in range(height):
        line_chars = []
        for _ in range(width):
            color = random.choice(palette)
            line_chars.append(f"{color}{BLOCK}{RESET}")
        lines.append("".join(line_chars))
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate random ANSI art.")
    parser.add_argument("--width", type=int, default=40, help="Canvas width (default: 40)")
    parser.add_argument("--height", type=int, default=10, help="Canvas height (default: 10)")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    art = generate_art(width=args.width, height=args.height)
    print(art)


if __name__ == "__main__":
    main()
