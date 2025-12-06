#!/usr/bin/env python3
"""
UUID Shortener utility.

Provides two public functions:
- ``encode_uuid(uuid_str)`` → short Base‑62 string
- ``decode_uuid(short_str)`` → canonical UUID string

The module can also be executed as a tiny CLI:

    python -m shortener encode <uuid>
    python -m shortener decode <short>
"""

import sys
import uuid
from typing import Any

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(BASE62_ALPHABET)


def _int_to_base62(num: int) -> str:
    """Convert a non‑negative integer to a Base‑62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    chars = []
    while num:
        num, rem = divmod(num, BASE)
        chars.append(BASE62_ALPHABET[rem])
    return "".join(reversed(chars))


def _base62_to_int(s: str) -> int:
    """Convert a Base‑62 string back to an integer."""
    num = 0
    for char in s:
        num = num * BASE + BASE62_ALPHABET.index(char)
    return num


def encode_uuid(uuid_str: str) -> str:
    """Encode a UUID string (with hyphens) to a Base‑62 short string.

    Args:
        uuid_str: Standard UUID representation, e.g. ``"123e4567-e89b-12d3-a456-426614174000"``.
    Returns:
        A Base‑62 encoded string without hyphens.
    """
    u = uuid.UUID(uuid_str)
    return _int_to_base62(u.int)


def decode_uuid(short_str: str) -> str:
    """Decode a Base‑62 short string back to the canonical UUID string.

    Args:
        short_str: The Base‑62 representation produced by ``encode_uuid``.
    Returns:
        The standard hyphenated UUID string.
    """
    num = _base62_to_int(short_str)
    u = uuid.UUID(int=num)
    return str(u)


def _cli() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in {"encode", "decode"}:
        print("Usage: python -m shortener <encode|decode> <value>")
        sys.exit(1)
    command, value = sys.argv[1], sys.argv[2]
    if command == "encode":
        print(encode_uuid(value))
    else:
        print(decode_uuid(value))


if __name__ == "__main__":
    _cli()
