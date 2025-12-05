import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Regular expression that matches most common emoji characters.
# This is a simplified pattern covering the main emoji blocks.
_EMOJI_PATTERN = re.compile(
    "[\U0001F600-\U0001F64F]"  # Emoticons
    "|[\U0001F300-\U0001F5FF]"  # Misc Symbols and Pictographs
    "|[\U0001F680-\U0001F6FF]"  # Transport & Map Symbols
    "|[\U0001F700-\U0001F77F]"  # Alchemical Symbols
    "|[\U0001F780-\U0001F7FF]"  # Geometric Shapes Extended
    "|[\U0001F800-\U0001F8FF]"  # Supplemental Arrows-C
    "|[\U0001FA00-\U0001FA6F]"  # Chess Symbols
    "|[\U0001FA70-\U0001FAFF]"  # Symbols and Pictographs Extended-A
    "|[\U00002702-\U000027B0]"  # Dingbats
    "|[\U000024C2-\U0001F251]"  # Enclosed characters
)


def count_emojis(text: str) -> dict[str, int]:
    """Return a mapping of emoji → occurrence count.

    Parameters
    ----------
    text: str
        The input text to scan.

    Returns
    -------
    dict[str, int]
        Emoji frequencies sorted by descending count.
    """
    matches = _EMOJI_PATTERN.findall(text)
    counter = Counter(matches)
    # Sort by count descending, then emoji codepoint for deterministic order
    sorted_items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return dict(sorted_items)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count emojis in a text file.")
    parser.add_argument("filepath", type=Path, help="Path to the UTF‑8 text file.")
    args = parser.parse_args(argv)

    try:
        content = args.filepath.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        return 1

    counts = count_emojis(content)
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
