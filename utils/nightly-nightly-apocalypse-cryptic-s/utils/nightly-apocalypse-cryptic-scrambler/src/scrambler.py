"""
scrambler.py - Simple substitution cipher for post‑apocalyptic notes.
"""

import string
from typing import Dict

# Fixed substitution mapping (A-Z)
_ENCRYPT_MAP: Dict[str, str] = {
    'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R', 'E': 'T',
    'F': 'Y', 'G': 'U', 'H': 'I', 'I': 'O', 'J': 'P',
    'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F', 'O': 'G',
    'P': 'H', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
    'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B', 'Y': 'N',
    'Z': 'M'
}
# Build reverse map
_DECRYPT_MAP = {v: k for k, v in _ENCRYPT_MAP.items()}


def _translate(text: str, mapping: Dict[str, str]) -> str:
    """Translate *text* using *mapping* while preserving case.

    Non‑alphabetic characters are returned unchanged.
    """
    result = []
    for ch in text:
        if ch.upper() in mapping:
            enc = mapping[ch.upper()]
            result.append(enc if ch.isupper() else enc.lower())
        else:
            result.append(ch)
    return ''.join(result)


def encrypt(text: str) -> str:
    """Encrypt plain text using the fixed substitution cipher."""
    return _translate(text, _ENCRYPT_MAP)


def decrypt(text: str) -> str:
    """Decrypt cipher text back to plain text."""
    return _translate(text, _DECRYPT_MAP)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt or decrypt messages for the apocalypse.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the input")
    group.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the input")
    parser.add_argument("message", help="Message to process")
    args = parser.parse_args()
    if args.encrypt:
        print(encrypt(args.message))
    else:
        print(decrypt(args.message))
