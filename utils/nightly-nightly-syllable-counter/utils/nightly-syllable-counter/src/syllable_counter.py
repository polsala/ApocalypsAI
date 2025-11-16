"""syllable_counter.py

A tiny, dependency‑free utility that estimates the number of syllables in an English word.

The algorithm is deliberately simple:
  1. Count contiguous vowel groups (a, e, i, o, u, y).
  2. Adjust for a trailing silent "e".
  3. Enforce a minimum of one syllable.

It is **not** a substitute for a full phonetic dictionary, but it is sufficient for quick
readability checks, poetry helpers, and CI‑friendly offline usage.
"""

import re
from typing import List

VOWEL_REGEX = re.compile(r"[aeiouy]+", re.IGNORECASE)

def _vowel_groups(word: str) -> List[str]:
    """Return a list of contiguous vowel groups found in *word*.

    Example:
        >>> _vowel_groups("beautiful")
        ['e', 'a', 'u', 'i']
    """
    return VOWEL_REGEX.findall(word)

def count_syllables(word: str) -> int:
    """Estimate the number of syllables in *word*.

    The heuristic follows these steps:
    1. Lower‑case the word.
    2. Count vowel groups.
    3. If the word ends with a silent "e" (and has more than one group), subtract one.
    4. Ensure at least one syllable is returned.

    Parameters
    ----------
    word: str
        The word to evaluate. Non‑alphabetic characters are ignored.

    Returns
    -------
    int
        Estimated syllable count (minimum 1).
    """
    if not word:
        return 0

    # Strip non‑alphabetic characters (punctuation, numbers, etc.)
    cleaned = re.sub(r"[^a-zA-Z]", "", word).lower()
    if not cleaned:
        return 0

    groups = _vowel_groups(cleaned)
    syllable_count = len(groups)

    # Silent 'e' adjustment: if word ends with 'e' and we have more than one group,
    # assume the trailing 'e' does not form its own syllable.
    if cleaned.endswith("e") and syllable_count > 1:
        syllable_count -= 1

    # Ensure at least one syllable for non‑empty words.
    return max(syllable_count, 1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Estimate syllable count for a given word.")
    parser.add_argument("word", help="Word to evaluate")
    args = parser.parse_args()
    print(count_syllables(args.word))
