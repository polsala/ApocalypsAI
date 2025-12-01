#!/usr/bin/env python3
"""rot13.py – Encode or decode strings using the ROT13 cipher.

Usage:
    python -m utils.nightly-rot13-encoder.src.rot13 "some text"
    python -m utils.nightly-rot13-encoder.src.rot13 --decode "some text"
"""

import argparse
import sys
from typing import List


def _rot13_char(c: str) -> str:
    """Return the ROT13 transformation of a single character."""
    if "a" <= c <= "z":
        return chr(((ord(c) - ord('a') + 13) % 26) + ord('a'))
    if "A" <= c <= "Z":
        return chr(((ord(c) - ord('A') + 13) % 26) + ord('A'))
    return c


def rot13(text: str) -> str:
    """Apply ROT13 to the entire string and return the result."""
    return "".join(_rot13_char(ch) for ch in text)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Encode or decode a string using ROT13.")
    parser.add_argument("text", help="The text to encode/decode.")
    parser.add_argument(
        "--decode",
        action="store_true",
        help="Flag is kept for semantic clarity; ROT13 is symmetric.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    # ROT13 is symmetric; the flag does not change the algorithm.
    result = rot13(args.text)
    print(result)


if __name__ == "__main__":
    main()
