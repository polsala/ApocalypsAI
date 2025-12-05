import argparse
import random
from typing import List, Optional

DEFAULT_ADJECTIVES = [
    "fluffy",
    "spooky",
    "brave",
    "silly",
    "mysterious",
    "cheerful",
    "grumpy",
    "zany",
]

DEFAULT_NOUNS = [
    "unicorn",
    "robot",
    "dragon",
    "wizard",
    "pirate",
    "ninja",
    "goblin",
    "penguin",
]


def generate_username(
    adjectives: Optional[List[str]] = None,
    nouns: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> str:
    """Generate a whimsical username.

    The function picks a random adjective and noun from the provided lists (or defaults)
    and appends a two‑digit random number (00‑99).

    Parameters
    ----------
    adjectives: list of str, optional
        Custom adjectives to choose from.
    nouns: list of str, optional
        Custom nouns to choose from.
    seed: int, optional
        Seed for the random generator to make output deterministic.

    Returns
    -------
    str
        The generated username, e.g. "fluffy-unicorn42".
    """
    if seed is not None:
        random.seed(seed)
    adj_list = adjectives or DEFAULT_ADJECTIVES
    noun_list = nouns or DEFAULT_NOUNS
    adjective = random.choice(adj_list)
    noun = random.choice(noun_list)
    number = random.randint(0, 99)
    return f"{adjective}-{noun}{number:02d}"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate whimsical usernames.")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of usernames to generate (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for deterministic output",
    )
    parser.add_argument(
        "--adjectives",
        type=str,
        nargs="*",
        help="Custom adjectives (space‑separated)",
    )
    parser.add_argument(
        "--nouns",
        type=str,
        nargs="*",
        help="Custom nouns (space‑separated)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    adjectives = args.adjectives if args.adjectives else None
    nouns = args.nouns if args.nouns else None
    for _ in range(args.count):
        username = generate_username(adjectives=adjectives, nouns=nouns, seed=args.seed)
        print(username)


if __name__ == "__main__":
    main()
