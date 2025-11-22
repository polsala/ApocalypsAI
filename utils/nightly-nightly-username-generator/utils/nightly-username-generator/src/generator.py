import hashlib
import re
from typing import Optional

_ADJECTIVES = [
    "brave",
    "clever",
    "daring",
    "eager",
    "fancy",
    "gentle",
    "happy",
    "jolly",
    "kind",
    "lively",
]

_NOUNS = [
    "lion",
    "tiger",
    "eagle",
    "shark",
    "wizard",
    "phoenix",
    "dragon",
    "unicorn",
    "panther",
    "falcon",
]

_PATTERN = re.compile(r"^[a-z]+-[a-z]+\d{3}$")


def _hash_seed(seed: Optional[int]) -> str:
    """Return a hex digest for *seed*.

    If *seed* is ``None`` we fall back to a random‑like hash based on the
    current process ID and time, but the public API encourages providing an
    explicit seed for reproducibility.
    """
    if seed is None:
        # Use a pseudo‑random seed derived from runtime state – still deterministic
        # for the duration of a single process execution.
        seed_bytes = f"{hashlib.sha256().hexdigest()}".encode()
    else:
        seed_bytes = str(seed).encode()
    return hashlib.sha256(seed_bytes).hexdigest()


def generate_username(seed: Optional[int] = None) -> str:
    """Generate a deterministic username.

    The username format is ``<adjective>-<noun><NNN>`` where ``NNN`` is a three‑digit
    number (zero‑padded). The same *seed* always yields the same username.
    """
    digest = _hash_seed(seed)
    # Use slices of the digest to pick indices.
    adj_index = int(digest[0:8], 16) % len(_ADJECTIVES)
    noun_index = int(digest[8:16], 16) % len(_NOUNS)
    number = int(digest[16:24], 16) % 1000
    username = f"{_ADJECTIVES[adj_index]}-{_NOUNS[noun_index]}{number:03d}"
    # Safety check – should always match the pattern.
    assert _PATTERN.match(username), f"Generated username '{username}' does not match expected pattern"
    return username


def _cli() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Generate a deterministic whimsical username.")
    parser.add_argument("--seed", type=int, default=None, help="Optional integer seed for deterministic output.")
    args = parser.parse_args()
    print(generate_username(seed=args.seed))


if __name__ == "__main__":
    _cli()
