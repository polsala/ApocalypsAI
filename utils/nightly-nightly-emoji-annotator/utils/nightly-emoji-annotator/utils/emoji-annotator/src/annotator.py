"""
emoji_annotator – Append emojis to lines based on keyword detection.

Run as a module:
    python -m emoji_annotator.src.annotator INPUT_PATH OUTPUT_PATH
"""

import argparse
import sys
from pathlib import Path
from typing import Dict

# Simple keyword → emoji map
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "error": "❌",
    "warning": "⚠️",
    "success": "✅",
    "info": "ℹ️",
    "debug": "🐞",
    "todo": "📝",
    "fix": "🔧",
    "love": "❤️",
    "fire": "🔥",
}

def annotate_line(line: str) -> str:
    """Return the line with an appended emoji if a keyword is found.

    The first keyword (in map order) that appears as a whole word (case‑insensitive)
    triggers its emoji. If none match, the original line is returned unchanged.
    """
    lowered = line.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        # split on whitespace to approximate whole‑word matching
        if keyword in lowered.split():
            return f"{line.rstrip()} {emoji}"
    return line.rstrip()

def process_file(input_path: Path, output_path: Path) -> None:
    """Read input_path, annotate each line, write to output_path."""
    with input_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(annotate_line(line) + "\n")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Annotate text lines with emojis.")
    parser.add_argument("input", type=Path, help="Path to input text file")
    parser.add_argument("output", type=Path, help="Path to write annotated output")
    args = parser.parse_args(argv)

    if not args.input.is_file():
        sys.stderr.write(f"Input file not found: {args.input}\n")
        return 1

    try:
        process_file(args.input, args.output)
    except Exception as exc:  # pragma: no cover
        sys.stderr.write(f"Failed to process files: {exc}\n")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
