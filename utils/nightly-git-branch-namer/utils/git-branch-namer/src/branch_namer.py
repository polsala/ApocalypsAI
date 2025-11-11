"""git-branch-namer – generate concise kebab‑case branch names from commit messages.

The module provides a single public function ``suggest_branch_name`` and a tiny CLI wrapper.
"""

import argparse
import re
from typing import List

_MAX_LENGTH = 30  # maximum characters for the branch name
_MAX_WORDS = 4    # maximum words to keep from the commit message


def _clean_message(message: str) -> List[str]:
    """Normalise *message* and return a list of words.

    Steps:
    1. Lower‑case the string.
    2. Replace any non‑alphanumeric character (except spaces) with a space.
    3. Split on whitespace and filter out empty tokens.
    """
    lowered = message.lower()
    # Replace punctuation/special chars with space
    sanitized = re.sub(r"[^a-z0-9\s]", " ", lowered)
    words = [w for w in sanitized.split() if w]
    return words


def suggest_branch_name(commit_message: str) -> str:
    """Return a kebab‑case branch name derived from *commit_message*.

    The algorithm is deterministic and offline – no external services are called.
    """
    words = _clean_message(commit_message)
    if not words:
        raise ValueError("Commit message must contain at least one alphanumeric character")

    # Take up to _MAX_WORDS words
    selected = words[:_MAX_WORDS]
    candidate = "-".join(selected)

    # Truncate to _MAX_LENGTH while keeping whole words
    if len(candidate) > _MAX_LENGTH:
        # Reduce words one by one until it fits
        while selected and len("-".join(selected)) > _MAX_LENGTH:
            selected.pop()
        candidate = "-".join(selected)

    # Ensure the branch starts with a letter (Git requirement)
    if not candidate[0].isalpha():
        # Prepend a generic prefix
        candidate = f"branch-{candidate}"

    return candidate


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a kebab‑case Git branch name from a commit message.")
    parser.add_argument("message", help="Commit message to convert")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        branch = suggest_branch_name(args.message)
        print(branch)
    except ValueError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
