"""phrase‑passphrase‑generator
================================
Utility to deterministically derive a password from a human‑readable phrase and a salt.

The algorithm is deliberately simple and **offline‑only**:
1. Concatenate ``phrase`` and ``salt``.
2. Repeat the concatenated string until the desired ``length`` is met.
3. Filter characters according to the requested ``charset``.
4. If filtering removes too many characters, pad with ``'x'``.

The same inputs always produce the same output, making it suitable for reproducible
password generation without any external services.
"""

import argparse
import sys
from typing import Literal

Charset = Literal["alnum", "alpha", "numeric"]

def _filter_charset(s: str, charset: Charset) -> str:
    """Return a string containing only characters allowed by *charset*.

    - ``alnum``  – letters and digits
    - ``alpha``  – letters only
    - ``numeric`` – digits only
    """
    if charset == "alnum":
        return "".join(c for c in s if c.isalnum())
    if charset == "alpha":
        return "".join(c for c in s if c.isalpha())
    if charset == "numeric":
        return "".join(c for c in s if c.isdigit())
    raise ValueError(f"Unsupported charset: {charset}")


def generate_password(
    phrase: str,
    salt: str,
    length: int = 16,
    charset: Charset = "alnum",
) -> str:
    """Generate a deterministic password.

    Parameters
    ----------
    phrase: str
        Human‑readable passphrase.
    salt: str
        Additional entropy – can be anything (e.g., a site name).
    length: int, default 16
        Desired password length.
    charset: {'alnum', 'alpha', 'numeric'}, default 'alnum'
        Character set to restrict the output.
    """
    if length <= 0:
        raise ValueError("length must be positive")

    combined = phrase + salt
    # Repeat the combined string enough times and truncate to *length*
    repeated = (combined * ((length // len(combined)) + 1))[:length]

    filtered = _filter_charset(repeated, charset)
    # Pad with 'x' if filtering removed too many characters
    while len(filtered) < length:
        filtered += "x"
    return filtered[:length]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic phrase‑based password generator")
    parser.add_argument("--phrase", required=True, help="Base phrase (human readable)")
    parser.add_argument("--salt", required=True, help="Salt value to add entropy")
    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Desired password length (default: 16)",
    )
    parser.add_argument(
        "--charset",
        choices=["alnum", "alpha", "numeric"],
        default="alnum",
        help="Character set to restrict the password (default: alnum)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        pwd = generate_password(
            phrase=args.phrase,
            salt=args.salt,
            length=args.length,
            charset=args.charset,  # type: ignore[arg-type]
        )
    except Exception as exc:  # pragma: no cover – defensive
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(pwd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
