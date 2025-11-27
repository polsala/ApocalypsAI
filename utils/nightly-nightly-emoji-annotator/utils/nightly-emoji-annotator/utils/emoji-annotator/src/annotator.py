"""emoji_annotator – Append context‑aware emojis to text lines.

This module provides two public callables:

* ``annotate_line(line: str) -> str`` – Return the line with an emoji.
* ``process_file(input_path: str, output_path: str) -> None`` – Read ``input_path`` line‑by‑line,
  write the annotated lines to ``output_path``.

The CLI entry‑point is ``python -m emoji_annotator <in> <out>``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

# Simple keyword → emoji mapping (order matters – first match wins)
_KEYWORD_EMOJI_MAP: List[Tuple[List[str], str]] = [
    ("happy joy glad".split(), "😊"),
    ("sad sorrow upset".split(), "😢"),
    ("love heart".split(), "❤️"),
    ("angry mad furious".split(), "😠"),
    ("surprise wow".split(), "😲"),
]

_DEFAULT_EMOJI = "🤔"


def _pick_emoji(line: str) -> str:
    """Return the first matching emoji for *line* or the default.

    Matching is case‑insensitive and looks for whole‑word occurrences.
    """
    lowered = line.lower()
    for keywords, emoji in _KEYWORD_EMOJI_MAP:
        for kw in keywords:
            if kw in lowered:
                return emoji
    return _DEFAULT_EMOJI


def annotate_line(line: str) -> str:
    """Append an appropriate emoji to *line*.

    The trailing newline (if any) is preserved.
    """
    # Preserve original newline characters
    newline = "" if not line.endswith("\n") else "\n"
    stripped = line.rstrip("\n")
    emoji = _pick_emoji(stripped)
    return f"{stripped} {emoji}{newline}"


def process_file(input_path: str | Path, output_path: str | Path) -> None:
    """Read *input_path*, write annotated lines to *output_path*.

    Raises ``FileNotFoundError`` if the input does not exist.
    """
    inp = Path(input_path)
    out = Path(output_path)
    if not inp.is_file():
        raise FileNotFoundError(f"Input file not found: {inp}")
    with inp.open("r", encoding="utf-8") as fin, out.open("w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(annotate_line(line))


def _cli() -> None:
    if len(sys.argv) != 3:
        prog = Path(sys.argv[0]).name
        print(f"Usage: python -m {prog} <input_file> <output_file>")
        sys.exit(2)
    input_file, output_file = sys.argv[1], sys.argv[2]
    try:
        process_file(input_file, output_file)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
