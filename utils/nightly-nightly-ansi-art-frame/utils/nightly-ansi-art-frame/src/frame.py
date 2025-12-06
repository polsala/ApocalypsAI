import argparse
import hashlib
from typing import Literal

Style = Literal["single", "double", "bold"]

_BORDERS = {
    "single": {
        "tl": "┌",
        "tr": "┐",
        "bl": "└",
        "br": "┘",
        "h": "─",
        "v": "│",
    },
    "double": {
        "tl": "╔",
        "tr": "╗",
        "bl": "╚",
        "br": "╝",
        "h": "═",
        "v": "║",
    },
    "bold": {
        "tl": "+",
        "tr": "+",
        "bl": "+",
        "br": "+",
        "h": "-",
        "v": "|",
    },
}


def _choose_style(text: str) -> Style:
    """Deterministically pick a style based on the SHA‑256 hash of *text*.

    The hash is converted to an integer and modulo‑ed by the number of styles.
    """
    digest = hashlib.sha256(text.encode()).digest()
    idx = digest[0] % len(_BORDERS)
    return list(_BORDERS.keys())[idx]  # type: ignore[return-value]


def frame_text(text: str, style: Style | None = None) -> str:
    """Return *text* wrapped in a box of the given *style*.

    If *style* is ``None`` the style is chosen deterministically via ``_choose_style``.
    Multi‑line input is supported – each line is padded to the width of the longest line.
    """
    if style is None:
        style = _choose_style(text)
    border = _BORDERS[style]

    lines = text.splitlines() or [""]
    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]

    top = f"{border['tl']}{border['h'] * (max_len + 2)}{border['tr']}"
    bottom = f"{border['bl']}{border['h'] * (max_len + 2)}{border['br']}"
    middle = "\n".join(f"{border['v']} {line} {border['v']}" for line in padded)
    return f"{top}\n{middle}\n{bottom}"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wrap text in an ASCII/ANSI frame.")
    parser.add_argument("text", help="Text to frame. Use quotes for spaces.")
    parser.add_argument(
        "--style",
        choices=list(_BORDERS.keys()),
        default=None,
        help="Box style (single, double, bold). If omitted, style is auto‑selected.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = frame_text(args.text, args.style)  # type: ignore[arg-type]
    print(result)


if __name__ == "__main__":
    main()
