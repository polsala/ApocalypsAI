"""rot13_encoder

Provides a simple ROT13 implementation and a tiny CLI wrapper.

The ROT13 algorithm shifts each alphabetical character by 13 places; it is its own inverse.
"""

import sys
from typing import Iterable

def _rot13_char(ch: str) -> str:
    """Return the ROT13 transformation of a single character."""
    if 'a' <= ch <= 'z':
        return chr(((ord(ch) - ord('a') + 13) % 26) + ord('a'))
    if 'A' <= ch <= 'Z':
        return chr(((ord(ch) - ord('A') + 13) % 26) + ord('A'))
    return ch

def rot13(text: str) -> str:
    """Encode (or decode) *text* using ROT13.

    The operation is symmetric – applying it twice returns the original string.
    """
    return ''.join(_rot13_char(ch) for ch in text)

def _iter_input(args: Iterable[str]) -> str:
    """Combine CLI arguments or stdin into a single string.

    * If arguments are supplied, they are joined with spaces.
    * Otherwise, the function reads the entire stdin stream.
    """
    if args:
        return ' '.join(args)
    # Mock rationale: reading from stdin keeps the utility pure‑offline and testable.
    return sys.stdin.read().rstrip('\n')

def main() -> None:
    """Entry point for the ``python -m src.rot13_encoder`` command.

    It prints the ROT13‑encoded version of the supplied text.
    """
    input_text = _iter_input(sys.argv[1:])
    print(rot13(input_text))

if __name__ == "__main__":
    main()
