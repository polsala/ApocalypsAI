"""
deterministic-passphrase-generator

Provides a function to generate a reproducible password from a master phrase.
"""

import argparse
import base64
import hashlib
from typing import Any


def generate_password(master_phrase: str, length: int = 12) -> str:
    """
    Generate a deterministic password.

    Args:
        master_phrase: The secret master phrase.
        length: Desired password length (default 12). Must be >0.

    Returns:
        A password string of the requested length.
    """
    if length <= 0:
        raise ValueError("length must be positive")
    # Compute SHA-256 hash
    digest = hashlib.sha256(master_phrase.encode("utf-8")).digest()
    # Base64 url-safe encoding, remove padding
    b64 = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    # Return truncated string
    return b64[:length]


def _parse_args(args: Any = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic password from a master phrase."
    )
    parser.add_argument("master_phrase", help="Master phrase to derive the password from.")
    parser.add_argument(
        "--length",
        type=int,
        default=12,
        help="Length of the generated password (default: 12).",
    )
    return parser.parse_args(args)


def main() -> None:
    ns = _parse_args()
    try:
        pwd = generate_password(ns.master_phrase, ns.length)
        print(pwd)
    except Exception as e:
        # Simple error handling for CLI usage
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
