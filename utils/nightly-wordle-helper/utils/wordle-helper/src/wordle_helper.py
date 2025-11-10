"""wordle_helper.py

A tiny helper library for the popular Wordle game.

It ships with a static list of common 5‑letter English words so that the
module works completely offline – perfect for deterministic unit tests.
"""

from __future__ import annotations

from typing import List

# Mock rationale: using a static small word list for deterministic offline tests.
WORD_LIST: List[str] = [
    "apple",
    "angle",
    "baker",
    "cigar",
    "crane",
    "drape",
    "eagle",
    "flame",
    "glare",
    "grape",
    "heart",
    "joker",
    "knock",
    "lemon",
    "mango",
    "nerve",
    "ocean",
    "piano",
    "queen",
    "raven",
    "scale",
    "tiger",
    "ultra",
    "vivid",
    "waltz",
    "xenon",
    "yacht",
    "zebra",
]

def _normalize(word: str) -> str:
    """Return a lower‑cased version of *word*.

    The helper works case‑insensitively, but the internal word list is already
    lower‑cased. This function centralises the conversion for future extensions.
    """
    return word.lower()

def filter_words(pattern: str, excluded: str) -> List[str]:
    """Return words from :data:`WORD_LIST` that match *pattern* and avoid *excluded*.

    Parameters
    ----------
    pattern:
        A 5‑character string where known letters are placed verbatim and unknown
        slots are represented by ``?`` or ``_``. Case‑insensitive.
    excluded:
        A string of letters that must **not** appear anywhere in the candidate
        word. Case‑insensitive.

    Returns
    -------
    List[str]
        All matching words in alphabetical order.
    """
    if len(pattern) != 5:
        raise ValueError("Pattern must be exactly 5 characters long")

    pattern = _normalize(pattern)
    excluded_set = set(_normalize(excluded))
    wildcards = {"?", "_"}

    matches: List[str] = []
    for word in WORD_LIST:
        w = _normalize(word)
        # Exclude words containing any forbidden letter
        if excluded_set.intersection(set(w)):
            continue
        # Position‑by‑position check
        for p_char, w_char in zip(pattern, w):
            if p_char in wildcards:
                continue
            if p_char != w_char:
                break
        else:
            matches.append(word)
    return sorted(matches)

__all__ = ["filter_words"]
