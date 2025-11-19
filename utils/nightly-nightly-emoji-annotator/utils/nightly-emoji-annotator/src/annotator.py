"""Emoji Annotator utility.

Splits text into sentences and appends a random emoji after each sentence.
"""

import argparse
import random
import re
import sys
from pathlib import Path

EMOJIS = [
    "😀", "😂", "🥳", "🤖", "🌟", "🚀", "🧩", "🍕", "🐍", "💡"
]

_SENTENCE_RE = re.compile(r'(?<=[.!?])\s+')

def annotate_text(text: str) -> str:
    """Return text with a random emoji appended after each sentence."""
    sentences = _SENTENCE_RE.split(text.strip())
    annotated = []
    for sentence in sentences:
        if not sentence:
            continue
        emoji = random.choice(EMOJIS)
        annotated.append(f"{sentence} {emoji}")
    return " ".join(annotated)

def main(argv=None):
    parser = argparse.ArgumentParser(description="Annotate sentences with emojis.")
    parser.add_argument("--input", "-i", type=Path, help="Path to input text file (default: stdin).")
    parser.add_argument("--output", "-o", type=Path, help="Path to output file (default: stdout).")
    args = parser.parse_args(argv)

    # Read input
    if args.input:
        text = args.input.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    result = annotate_text(text)

    # Write output
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        sys.stdout.write(result)

if __name__ == "__main__":
    main()
