#!/usr/bin/env python3
"""
rot13 utility – apply ROT13 cipher.

Provides a library function :func:`rot13` and a small CLI that reads either
command‑line arguments or stdin and prints the transformed text.
"""

import sys
from typing import Iterable


def rot13(text: str) -> str:
    """Return the ROT13 transformation of *text*.

    Only the 26 English letters are rotated; all other characters are left
    unchanged.
    """
    result = []
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:  # A‑Z
            result.append(chr(((o - 65 + 13) % 26) + 65))
        elif 97 <= o <= 122:  # a‑z
            result.append(chr(((o - 97 + 13) % 26) + 97))
        else:
            result.append(ch)
    return "".join(result)


def _iter_input() -> Iterable[str]:
    """Yield input lines.

    If any command‑line arguments are supplied they are joined with spaces and
    yielded as a single line. Otherwise the function reads from *stdin* line by
    line.
    """
    if len(sys.argv) > 1:
        # All arguments after the script name are treated as a single input string
        yield " ".join(sys.argv[1:])
    else:
        for line in sys.stdin:
            yield line.rstrip("\n")


def main() -> None:
    """CLI entry point – print ROT13‑encoded lines to stdout."""
    for line in _iter_input():
        print(rot13(line))


if __name__ == "__main__":
    main()
