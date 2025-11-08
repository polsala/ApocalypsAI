#!/usr/bin/env python3
"""text-similarity-cli – compute Jaccard similarity between two strings.

Provides:
- `jaccard_similarity(text_a: str, text_b: str) -> float`
- `main(argv: list[str] | None = None) -> int` – CLI entry point.
"""

import argparse
import sys
from typing import Iterable, Set


def _tokenise(text: str) -> Set[str]:
    """Return a set of lower‑cased whitespace tokens.

    Empty strings yield an empty set.
    """
    return {token.lower() for token in text.split() if token}


def jaccard_similarity(text_a: str, text_b: str) -> float:
    """Calculate Jaccard similarity between two texts.

    J(A, B) = |A ∩ B| / |A ∪ B|
    If both token sets are empty, similarity is defined as 1.0.
    """
    set_a = _tokenise(text_a)
    set_b = _tokenise(text_b)
    if not set_a and not set_b:
        return 1.0
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return len(intersection) / len(union)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text-similarity-cli",
        description="Compute Jaccard similarity between two strings."
    )
    parser.add_argument("text_a", help="First piece of text")
    parser.add_argument("text_b", help="Second piece of text")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    score = jaccard_similarity(args.text_a, args.text_b)
    # Print with 4 decimal places for readability
    print(f"{score:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
