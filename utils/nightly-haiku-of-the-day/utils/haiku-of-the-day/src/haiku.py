#!/usr/bin/env python3
"""
haiku_of_the_day: deterministic haiku generator based on date.
"""

import datetime
import hashlib
import random
from typing import List

# Simple word banks for each line syllable count (5‑7‑5)
LINE1_WORDS = [
    "autumn",
    "silent",
    "crimson",
    "soft",
    "bright",
    "golden",
    "lonely",
    "misty",
]
LINE2_WORDS = [
    "whispers",
    "shimmering",
    "fluttering",
    "glimmering",
    "dancing",
    "echoing",
    "wandering",
]
LINE3_WORDS = [
    "sunrise",
    "nightfall",
    "river",
    "mountain",
    "dreams",
    "shadows",
    "silence",
]

def _syllable(word: str) -> int:
    """Very rough syllable estimator: count vowel groups."""
    import re
    return len(re.findall(r"[aeiouy]+", word.lower()))

def _select_words(target_syllables: int, pool: List[str], rng: random.Random) -> str:
    """Select words from *pool* to reach *target_syllables* using a deterministic RNG.
    The algorithm shuffles the pool deterministically, then greedily picks words.
    """
    chosen: List[str] = []
    total = 0
    # Deterministic shuffle via sorting on a random key
    shuffled = sorted(pool, key=lambda _: rng.random())
    for word in shuffled:
        syl = _syllable(word)
        if total + syl <= target_syllables:
            chosen.append(word)
            total += syl
        if total == target_syllables:
            break
    # Fallback: repeat the first word if exact count not reached (unlikely with given pools)
    if total != target_syllables:
        first = pool[0]
        syl = _syllable(first)
        repeat = target_syllables // syl
        chosen = [first] * repeat
    return " ".join(chosen)

def generate_haiku(date: datetime.date = None) -> str:
    """Generate a haiku for *date* (defaults to today). Deterministic across runs.
    """
    if date is None:
        date = datetime.date.today()
    # Seed RNG with a hash of the ISO date string
    seed_bytes = hashlib.sha256(date.isoformat().encode()).digest()
    seed = int.from_bytes(seed_bytes[:4], "big")  # 32‑bit seed
    rng = random.Random(seed)

    line1 = _select_words(5, LINE1_WORDS, rng)
    line2 = _select_words(7, LINE2_WORDS, rng)
    line3 = _select_words(5, LINE3_WORDS, rng)
    return f"{line1}\n{line2}\n{line3}"

def main() -> None:
    print(generate_haiku())

if __name__ == "__main__":
    main()
