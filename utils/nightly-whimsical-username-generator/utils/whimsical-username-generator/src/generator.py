import argparse
import random
from typing import Optional

_ADJECTIVES = [
    "sparkly",
    "mystic",
    "zany",
    "brave",
    "cheerful",
    "dizzy",
    "eager",
    "fuzzy",
    "giddy",
    "hasty",
]

_NOUNS = [
    "otter",
    "phoenix",
    "unicorn",
    "panda",
    "dragon",
    "lemur",
    "tiger",
    "koala",
    "walrus",
    "sphinx",
]


def _pick_random(seq):
    """Return a random element from *seq* using the global random state.

    This helper exists solely to make the intent explicit and to aid testing
    (the test suite can monkey‑patch it if desired).
    """
    return random.choice(seq)


def generate_username(seed: Optional[int] = None) -> str:
    """Generate a whimsical username.

    Parameters
    ----------
    seed: Optional[int]
        If provided, the random module is seeded with this value, making the
        output deterministic. Useful for reproducible tests.

    Returns
    -------
    str
        A string in the form ``adjective-noun-number`` where *number* is a
        two‑digit integer (0‑99).
    """
    if seed is not None:
        random.seed(seed)
    adjective = _pick_random(_ADJECTIVES)
    noun = _pick_random(_NOUNS)
    number = random.randint(0, 99)
    return f"{adjective}-{noun}-{number:02d}"


def _cli():
    parser = argparse.ArgumentParser(description="Generate a whimsical username.")
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional integer seed for deterministic output.",
    )
    args = parser.parse_args()
    username = generate_username(seed=args.seed)
    print(username)


if __name__ == "__main__":
    _cli()
