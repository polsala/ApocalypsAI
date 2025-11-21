import argparse
import sys
from pathlib import Path
from typing import List, Tuple

# Mapping of keyword (lowercase) to emoji
KEYWORD_EMOJI_MAP = {
    "error": "😱",
    "fail": "😱",
    "failed": "😱",
    "failure": "😱",
    "warning": "⚠️",
    "warn": "⚠️",
    "success": "🎉",
    "passed": "🎉",
    "pass": "🎉",
}

def _detect_emoji(line: str) -> str:
    """Return the first matching emoji for *line* or an empty string.

    Matching is case‑insensitive and based on simple substring search.
    """
    lowered = line.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        if keyword in lowered:
            return f" {emoji}"  # prepend space for readability
    return ""

def annotate_lines(lines: List[str]) -> List[str]:
    """Annotate each line with an emoji according to keyword rules.

    Parameters
    ----------
    lines: List[str]
        Raw lines from the input file (including trailing newlines).

    Returns
    -------
    List[str]
        Annotated lines ready to be written back to a file.
    """
    annotated = []
    for line in lines:
        # Preserve original newline character
        newline = "" if not line.endswith("\n") else "\n"
        core = line.rstrip("\n")
        emoji = _detect_emoji(core)
        annotated.append(f"{core}{emoji}{newline}")
    return annotated

def annotate_file(input_path: Path, output_path: Path) -> None:
    """Read *input_path*, annotate its contents, and write to *output_path*.

    The function raises ``FileNotFoundError`` if the input does not exist.
    """
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    annotated = annotate_lines(lines)
    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(annotated)

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Annotate a text file with emojis based on simple keyword detection.")
    parser.add_argument("input", type=Path, help="Path to the input text file")
    parser.add_argument("output", type=Path, help="Path where the annotated file will be written")
    return parser.parse_args(argv)

def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        annotate_file(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
