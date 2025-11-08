"""username_generator

A tiny deterministic username generator.

Provides:
- `generate_username(seed: int) -> str`
- CLI entry point via `python -m utils.nightly-username-generator.src.generator`
"""

import argparse
import sys
from typing import List

# ---------------------------------------------------------------------------
# Syllable pools – whimsical but pronounceable.
# ---------------------------------------------------------------------------
_PREFIXES: List[str] = [
    "fluffy",
    "spiky",
    "crimson",
    "silent",
    "golden",
    "shadow",
    "bright",
    "misty",
    "jolly",
    "stormy",
]

_MIDDLES: List[str] = [
    "bunny",
    "dragon",
    "phoenix",
    "otter",
    "lynx",
    "tiger",
    "eagle",
    "wolf",
    "panda",
    "fox",
]

_SUFFIXES: List[str] = [
    "whisper",
    "blaze",
    "spark",
    "glimmer",
    "ripple",
    "storm",
    "frost",
    "ember",
    "quake",
    "zephyr",
]

# Simple Linear Congruential Generator for reproducible pseudo‑random numbers.
_LCG_A = 1664525
_LCG_C = 1013904223
_LCG_M = 2 ** 32


def _lcg(seed: int) -> int:
    """Return the next pseudo‑random integer given a seed.

    The algorithm is deterministic and does not rely on external randomness.
    """
    return (seed * _LCG_A + _LCG_C) % _LCG_M


def _choose(pool: List[str], seed: int) -> str:
    """Select an element from *pool* based on *seed*.

    The selection is deterministic: the same seed always picks the same element.
    """
    index = seed % len(pool)
    return pool[index]


def generate_username(seed: int) -> str:
    """Generate a whimsical username from an integer *seed*.

    The algorithm:
    1. Derive three pseudo‑random numbers using a simple LCG.
    2. Use each number to pick a prefix, middle, and suffix.
    3. Join them with a hyphen for readability.

    Example
    -------
    >>> generate_username(0)
    'fluffy-bunny-whisper'
    >>> generate_username(42)
    'fluffy-zebra'  # (actual output depends on the pools)
    """
    if not isinstance(seed, int):
        raise TypeError("seed must be an integer")

    # Derive three deterministic pseudo‑random numbers.
    s1 = _lcg(seed)
    s2 = _lcg(s1)
    s3 = _lcg(s2)

    prefix = _choose(_PREFIXES, s1)
    middle = _choose(_MIDDLES, s2)
    suffix = _choose(_SUFFIXES, s3)

    # For a bit of variety, sometimes omit the middle part.
    if seed % 5 == 0:
        return f"{prefix}-{suffix}"
    else:
        return f"{prefix}-{middle}-{suffix}"


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a whimsical, deterministic username from a numeric seed."
    )
    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Integer seed used to deterministically generate the username.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    try:
        username = generate_username(args.seed)
        print(username)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
