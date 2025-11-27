"""
nightly_emoji_annotator

Read lines from a file or stdin and prefix each line with a random emoji.
"""

import sys
import random
from pathlib import Path
from typing import Iterable, List

EMOJIS: List[str] = [
    "😀", "🚀", "🌟", "🔥", "💡", "🎉", "🧩", "🛠️", "📚", "⚡"
]


def annotate_line(line: str) -> str:
    """Return the line prefixed with a random emoji and a space."""
    emoji = random.choice(EMOJIS)
    return f"{emoji} {line.rstrip()}"


def iter_lines(source: Iterable[str]) -> Iterable[str]:
    """Yield annotated lines from an iterable of raw lines."""
    for line in source:
        yield annotate_line(line)


def main(argv: List[str] | None = None) -> int:
    """Entry point for the CLI.

    Args:
        argv: Optional list of arguments (excluding the program name).

    Returns:
        Exit code (0 on success, 1 on error).
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) > 1:
        print("Usage: python -m nightly_emoji_annotator [file]", file=sys.stderr)
        return 1

    if argv:
        path = Path(argv[0])
        if not path.is_file():
            print(f"File not found: {path}", file=sys.stderr)
            return 1
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    for annotated in iter_lines(lines):
        print(annotated)

    return 0


if __name__ == "__main__":
    sys.exit(main())
