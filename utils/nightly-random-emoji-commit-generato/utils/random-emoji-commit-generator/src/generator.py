"""random_emoji_commit_generator.src.generator

Utility to inject random emojis into a commit message.

The implementation is deliberately lightweight and uses only the Python standard library.
"""

import random
from typing import List

# A modest list of emojis that are safe to display in most terminals and Git logs.
_EMOJIS: List[str] = [
    "🚀", "✨", "🐛", "🛠️", "📦", "🔧", "🦄", "🐍", "⚡", "🔥", "💡", "✅",
]

def _choose_emojis(count: int, rng: random.Random) -> List[str]:
    """Return *count* emojis selected without replacement.

    If *count* exceeds the available emojis, the list is cycled.
    """
    if count <= 0:
        return []
    # Mock rationale: using rng.sample for deterministic selection when a seed is set.
    if count <= len(_EMOJIS):
        return rng.sample(_EMOJIS, count)
    # If more emojis are requested than we have, repeat the shuffled list.
    shuffled = _EMOJIS[:]
    rng.shuffle(shuffled)
    result = []
    while len(result) < count:
        result.extend(shuffled)
    return result[:count]

def generate_commit_message(message: str, count: int = 2, seed: int | None = None) -> str:
    """Insert *count* random emojis into *message*.

    Parameters
    ----------
    message: str
        The original commit message.
    count: int, optional
        Number of emojis to insert (default 2).
    seed: int | None, optional
        Seed for the random number generator.  Providing a seed makes the output
        deterministic – essential for reliable tests.

    Returns
    -------
    str
        The commit message with emojis sprinkled in.
    """
    rng = random.Random(seed)
    emojis = _choose_emojis(count, rng)
    if not emojis:
        return message

    words = message.split()
    # Determine insertion points: we will insert after random word indices.
    # Ensure we don't exceed the list length.
    insertion_indices = sorted(rng.sample(range(len(words) + 1), k=len(emojis)))
    # Mock rationale: sorting indices guarantees deterministic ordering of emojis.
    result_words: List[str] = []
    last_idx = 0
    for insert_idx, emoji in zip(insertion_indices, emojis):
        # Append words up to the insertion point.
        result_words.extend(words[last_idx:insert_idx])
        # Insert the emoji as its own token.
        result_words.append(emoji)
        last_idx = insert_idx
    # Append any remaining words.
    result_words.extend(words[last_idx:])
    return " ".join(result_words)

__all__ = ["generate_commit_message"]
