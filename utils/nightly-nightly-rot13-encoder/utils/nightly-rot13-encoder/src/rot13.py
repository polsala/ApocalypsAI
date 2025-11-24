#!/usr/bin/env python3
"""ROT13 encoder/decoder utility.

Provides a `rot13` function for library use and a small CLI for quick
conversions. The transformation is symmetric – applying it twice yields the
original text.
"""

import sys
import argparse

def rot13(text: str) -> str:
    """Return the ROT13 transformation of *text*.

    Non‑alphabetic characters are left unchanged.
    """
    trans = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
    )
    return text.translate(trans)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Encode or decode text using ROT13."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to encode/decode. If omitted, reads from stdin.",
    )
    args = parser.parse_args()

    if args.text is not None:
        input_text = args.text
    else:
        # Read entire stdin stream
        input_text = sys.stdin.read()

    output = rot13(input_text)
    print(output)


if __name__ == "__main__":
    main()
