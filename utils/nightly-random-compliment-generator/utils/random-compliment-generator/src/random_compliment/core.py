import random
from typing import List

_COMPLIMENTS: List[str] = [
    "You are a coding wizard!",
    "Your logic shines brighter than the sun.",
    "Every line you write is poetry.",
    "You make bugs tremble in fear.",
    "Your creativity knows no bounds.",
]


def get_random_compliment() -> str:
    """Return a random compliment from the predefined list.

    The function is deliberately simple to keep the utility lightweight.
    """
    return random.choice(_COMPLIMENTS)
