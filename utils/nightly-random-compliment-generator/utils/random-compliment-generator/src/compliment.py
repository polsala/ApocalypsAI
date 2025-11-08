import random
from typing import List

_COMPLIMENTS: List[str] = [
    "You have a brilliant mind!",
    "Your curiosity is contagious.",
    "You make complex problems look easy.",
    "Your code is poetry in motion.",
    "You bring sunshine to the terminal.",
]

def get_compliment() -> str:
    """Return a random compliment from the predefined list.

    The function is deliberately simple and deterministic when the
    random module is mocked (as done in the test suite).
    """
    return random.choice(_COMPLIMENTS)

if __name__ == "__main__":
    print(get_compliment())
