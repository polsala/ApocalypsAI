import itertools
from typing import List, Set

# A modest built‑in Scrabble‑style word list. In a real utility this could be swapped out for a full dictionary.
_WORDS: Set[str] = {
    "apple",
    "pear",
    "ape",
    "pea",
    "pale",
    "plea",
    "leap",
    "pal",
    "lap",
    "ale",
    "lea",
    "rap",
    "par",
    "car",
    "arc",
    "scar",
    "cars",
    "arcs",
    "ear",
    "are",
    "era",
    "reap",
    "rape",
    "pare",
    "spare",
    "spear",
    "pears",
    "reaps",
    "parse",
    "spare",
    "rasp",
    "spray",
    "prays",
    "pay",
    "ray",
    "spa",
    "sap",
    "asp",
    "ras",
}


def find_words(letters: str, min_len: int = 2) -> List[str]:
    """Return all words that can be built from *letters*.

    Parameters
    ----------
    letters: str
        The bag of letters (case‑insensitive). Duplicate letters are respected.
    min_len: int, optional
        Minimum word length to consider (default 2).

    Returns
    -------
    List[str]
        Words sorted by descending length then alphabetically.
    """
    letters = letters.lower()
    results: Set[str] = set()
    # Generate all permutations for each possible length.
    for length in range(min_len, len(letters) + 1):
        for perm in itertools.permutations(letters, length):
            candidate = "".join(perm)
            if candidate in _WORDS:
                results.add(candidate)
    # Sort: longest first, then alphabetical for ties.
    return sorted(results, key=lambda w: (-len(w), w))


def _cli() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Find Scrabble‑style words from a set of letters.")
    parser.add_argument("letters", help="Bag of letters (e.g., 'aple')")
    parser.add_argument("--min-len", type=int, default=2, help="Minimum word length (default: 2)")
    args = parser.parse_args()
    words = find_words(args.letters, min_len=args.min_len)
    for w in words:
        print(w)


if __name__ == "__main__":
    _cli()
