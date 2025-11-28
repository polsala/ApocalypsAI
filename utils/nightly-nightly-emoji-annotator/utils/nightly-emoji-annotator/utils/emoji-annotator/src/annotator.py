import sys
from pathlib import Path
from typing import Dict

# Simple keyword → emoji mapping
EMOJI_MAP: Dict[str, str] = {
    "coffee": "☕",
    "cat": "🐱",
    "dog": "🐶",
    "love": "❤️",
    "fire": "🔥",
    "star": "⭐",
    "pizza": "🍕",
    "music": "🎵",
    "book": "📚",
}

def annotate_text(text: str) -> str:
    """Replace standalone keywords in *text* with their emojis.

    The replacement is case‑insensitive and only matches whole words.
    """
    import re

    def repl(match: re.Match) -> str:
        word = match.group(0).lower()
        return EMOJI_MAP.get(word, match.group(0))

    pattern = re.compile(r"\\b(" + "|".join(map(re.escape, EMOJI_MAP.keys())) + r")\\b", re.IGNORECASE)
    return pattern.sub(repl, text)

def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m emoji_annotator <input_path> <output_path>")
        return 1
    input_path = Path(argv[0])
    output_path = Path(argv[1])
    try:
        raw = input_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read input file: {e}")
        return 1
    annotated = annotate_text(raw)
    try:
        output_path.write_text(annotated, encoding="utf-8")
    except Exception as e:
        print(f"Failed to write output file: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
