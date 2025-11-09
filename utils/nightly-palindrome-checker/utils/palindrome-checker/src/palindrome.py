"""Palindrome Checker utility.

Provides a function `is_palindrome` and a simple CLI.
"""

import sys
import re
from typing import Any

def _normalize(text: str) -> str:
    """Return a lowercase alphanumeric‑only version of *text*.
    # Mock rationale: using regex to strip non‑alphanumeric characters.
    """
    return re.sub(r'[^a-z0-9]', '', text.lower())

def is_palindrome(text: str) -> bool:
    """Return ``True`` if *text* is a palindrome ignoring case, spaces, and punctuation.
    """
    normalized = _normalize(text)
    return normalized == normalized[::-1]

def main(argv: Any = None) -> None:
    """CLI entry point.
    If no arguments are provided, reads from stdin.
    """
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        input_text = " ".join(argv)
    else:
        input_text = sys.stdin.read().strip()
    if is_palindrome(input_text):
        print("✅ Palindrome!")
    else:
        print("❌ Not a palindrome.")

if __name__ == "__main__":
    main()
