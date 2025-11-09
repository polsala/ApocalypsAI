"""wordle_helper.py

A tiny offline Wordle assistant.

Usage:
    python -m utils.wordle-helper.src.wordle_helper \
        --pattern <5‑char pattern with '?' for unknown> \
        [--exclude <comma‑separated letters>]

Example:
    python -m utils.wordle-helper.src.wordle_helper \
        --pattern c??e? --exclude a,b,d
"""

import argparse
import sys
from typing import List, Set

# A small curated list of common 5‑letter English words.
# In a real utility this could be replaced with a larger word list.
WORD_LIST = [
    "caper",
    "caste",
    "cater",
    "caves",
    "cello",
    "cents",
    "chase",
    "cheer",
    "chime",
    "civic",
    "clerk",
    "clone",
    "close",
    "coach",
    "coast",
    "cocoa",
    "couch",
    "crane",
    "crave",
    "creek",
    "creep",
    "crown",
    "crude",
    "cubes",
    "curry",
    "curve",
    "cycle",
]


def load_word_list() -> List[str]:
    """Return the built‑in word list.

    Keeping this in a function makes it easier to mock in tests.
    """
    return WORD_LIST


def filter_by_pattern(words: List[str], pattern: str) -> List[str]:
    """Return words matching the given pattern.

    `pattern` is a 5‑character string where known letters are placed
    and unknown positions are represented by '?'.
    """
    if len(pattern) != 5:
        raise ValueError("Pattern must be exactly 5 characters long.")
    result = []
    for w in words:
        match = True
        for pc, wc in zip(pattern.lower(), w.lower()):
            if pc != '?' and pc != wc:
                match = False
                break
        if match:
            result.append(w)
    return result


def filter_by_exclusions(words: List[str], exclusions: Set[str]) -> List[str]:
    """Remove any word containing a letter from `exclusions`."""
    if not exclusions:
        return words
    excl_lower = {e.lower() for e in exclusions}
    return [w for w in words if not any(ch in excl_lower for ch in w.lower())]


def parse_exclusions(arg: str) -> Set[str]:
    """Parse a comma‑separated string into a set of letters.

    Empty string returns an empty set.
    """
    if not arg:
        return set()
    # Mock rationale: split on commas, strip whitespace, ignore empty tokens.
    return {token.strip() for token in arg.split(',') if token.strip()}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline Wordle helper")
    parser.add_argument(
        "--pattern",
        required=True,
        help="5‑letter pattern with '?' for unknown positions (e.g., c??e?)",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Comma‑separated letters that are not in the word",
    )
    args = parser.parse_args(argv)

    try:
        words = load_word_list()
        words = filter_by_pattern(words, args.pattern)
        exclusions = parse_exclusions(args.exclude)
        words = filter_by_exclusions(words, exclusions)
        for w in words:
            print(w)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
