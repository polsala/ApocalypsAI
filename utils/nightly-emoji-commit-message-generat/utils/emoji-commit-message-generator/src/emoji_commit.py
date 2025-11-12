import os
import hashlib
from typing import List

EMOJI_LIST: List[str] = [
    "✨", "🚀", "🐛", "🔧", "📦", "🧹", "⚡", "🔥", "💡", "🛠️",
    "✅", "🔒", "🧪", "🎉", "🤖", "🧩", "📈", "🗑️", "🔀", "🧭"
]

def _hash_input(description: str) -> int:
    """Create a deterministic integer hash from description + optional seed."""
    seed = os.getenv("EMOJI_SEED", "")
    data = (description + seed).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return int(digest, 16)

def generate_message(description: str) -> str:
    """Return the original description appended with a deterministic emoji.

    Raises:
        ValueError: If the description is empty.
    """
    if not description:
        raise ValueError("Description must be non‑empty")
    idx = _hash_input(description) % len(EMOJI_LIST)
    emoji = EMOJI_LIST[idx]
    return f"{description} {emoji}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_commit \"<description>\"")
        sys.exit(1)
    print(generate_message(sys.argv[1]))
