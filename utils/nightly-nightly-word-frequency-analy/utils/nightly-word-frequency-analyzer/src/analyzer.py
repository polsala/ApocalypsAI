import argparse
import collections
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

WORD_RE = re.compile(r"\b\w+\b")


def _normalize(text: str) -> List[str]:
    """Return a list of lower‑cased words stripped of punctuation."""
    return [w.lower() for w in WORD_RE.findall(text)]


def count_words(text: str) -> Dict[str, int]:
    """Count occurrences of each word in *text*.

    The function is deterministic and pure – useful for unit‑testing.
    """
    words = _normalize(text)
    return dict(collections.Counter(words))


def top_n(counter: Dict[str, int], n: int) -> List[Tuple[str, int]]:
    """Return the *n* most common words sorted by count descending, then alphabetically."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def markdown_table(pairs: List[Tuple[str, int]]) -> str:
    """Render *pairs* as a markdown table with columns *Word* and *Count*."""
    lines = ["| Word | Count |", "|------|-------|"]
    for word, cnt in pairs:
        lines.append(f"| {word} | {cnt} |")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a markdown table of the most frequent words in a text file."
    )
    parser.add_argument("filepath", type=Path, help="Path to the input .txt file")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top words to display (default: 10)",
    )
    args = parser.parse_args(argv)

    try:
        text = args.filepath.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        return 1

    counter = count_words(text)
    pairs = top_n(counter, args.top)
    print(markdown_table(pairs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
