"""
fortune.py – Random Fortune Cookie Generator

Provides a CLI and a library function `get_fortune`.
"""

import argparse
import random
from typing import List, Optional, Dict

# Hard‑coded fortunes with categories
_FORTUNES: List[Dict[str, object]] = [
    {"text": "You will find great success in unexpected places.", "categories": ["wisdom", "inspiration"]},
    {"text": "A fresh start will put you on the path to greatness.", "categories": ["wisdom"]},
    {"text": "Never trust a computer you can't throw out a window.", "categories": ["humor", "tech"]},
    {"text": "Debugging is like being the detective in a crime movie where you are also the murderer.", "categories": ["humor", "tech"]},
    {"text": "Your code will compile on the first try. Keep believing.", "categories": ["tech", "inspiration"]},
    {"text": "Patience is a virtue, especially when waiting for CI.", "categories": ["humor", "wisdom"]},
]

def get_fortune(category: Optional[str] = None) -> str:
    """
    Return a random fortune. If ``category`` is supplied, only fortunes that include
    that category are considered. Raises ``ValueError`` if no fortunes match.
    """
    if category:
        filtered = [f for f in _FORTUNES if category.lower() in (c.lower() for c in f["categories"]))]
    else:
        filtered = _FORTUNES

    if not filtered:
        raise ValueError(f"No fortunes found for category '{category}'")

    choice = random.choice(filtered)
    return choice["text"]

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random fortune cookie message.")
    parser.add_argument(
        "--category",
        type=str,
        help="Filter fortunes by category (e.g., wisdom, humor, tech).",
    )
    return parser.parse_args()

def main() -> None:
    args = _parse_args()
    try:
        fortune = get_fortune(args.category)
        print(fortune)
    except ValueError as exc:
        print(exc)

if __name__ == "__main__":
    main()
