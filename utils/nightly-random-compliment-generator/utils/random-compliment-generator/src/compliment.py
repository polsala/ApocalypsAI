import argparse
import random
from typing import List, Dict, Optional


def _load_compliments() -> Dict[str, List[str]]:
    """Return a dictionary mapping categories to compliment lists.

    The data is kept inline to keep the utility self‑contained.
    """
    return {
        "general": [
            "You have a great sense of humor!",
            "Your curiosity is infectious.",
            "You make the world a better place just by being you.",
        ],
        "work": [
            "Your attention to detail is impressive.",
            "You turn challenges into opportunities.",
            "Your work ethic inspires the whole team.",
        ],
        "friendship": [
            "Your friendship is a gift to everyone around you.",
            "You always know the right thing to say.",
            "Your loyalty is unwavering.",
        ],
        "creativity": [
            "Your ideas are fresh and exciting.",
            "You see possibilities where others see obstacles.",
            "Your imagination knows no bounds.",
        ],
    }


def get_random_compliment(category: Optional[str] = None) -> str:
    """Return a random compliment.

    Args:
        category: Optional category to filter compliments. If ``None`` or unknown,
            a random category is chosen.
    """
    compliments = _load_compliments()
    if category and category in compliments:
        pool = compliments[category]
    else:
        # Flatten all compliments if category is missing/unknown
        pool = [c for lst in compliments.values() for c in lst]
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random compliment to stdout."
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Optional category (e.g., work, friendship, creativity).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    compliment = get_random_compliment(args.category)
    print(compliment)


if __name__ == "__main__":
    main()
