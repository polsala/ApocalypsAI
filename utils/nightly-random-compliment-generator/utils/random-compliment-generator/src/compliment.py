import random
import sys
from pathlib import Path

# List of compliments – feel free to extend!
_COMPLIMENTS = [
    "You are a brilliant problem‑solver!",
    "Your code reads like poetry.",
    "You make the world a better place, one commit at a time.",
    "Your debugging skills are legendary.",
    "You bring sunshine to the repository.",
]


def get_random_compliment() -> str:
    """Return a random compliment from the predefined list.

    The function is deliberately tiny to keep the utility lightweight.
    """
    return random.choice(_COMPLIMENTS)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Prints a random compliment to stdout and returns exit code 0.
    """
    if argv is None:
        argv = sys.argv[1:]
    # No arguments are required; ignore any provided.
    compliment = get_random_compliment()
    print(compliment)
    return 0


if __name__ == "__main__":
    sys.exit(main())
