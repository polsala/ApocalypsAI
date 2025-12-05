import hashlib
import sys
from typing import List

# A curated list of mood‑representing emojis.
EMOJIS: List[str] = [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
    "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
    "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩",
    "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣",
    "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬",
    "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "🤗", "🤔",
    "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦",
    "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴",
    "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈", "👿",
    "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "🤖", "🎃",
]

def _hash_to_index(value: str) -> int:
    """Hash *value* with SHA‑256 and map it into the range of ``EMOJIS``.

    The function is deliberately simple and deterministic across Python versions.
    """
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    # Convert the hex digest to an integer and take modulo the emoji count.
    return int(digest, 16) % len(EMOJIS)

def get_mood(value: str) -> str:
    """Return an emoji representing the *mood* for ``value``.

    Parameters
    ----------
    value: str
        Any string – commonly a date like ``"2025-01-01"``.

    Returns
    -------
    str
        A single emoji from the ``EMOJIS`` list.
    """
    index = _hash_to_index(value)
    return EMOJIS[index]

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-mood-generator.src.emoji_mood <string>")
        sys.exit(1)
    input_str = sys.argv[1]
    print(get_mood(input_str))

if __name__ == "__main__":
    _cli()
