import random
from typing import List

# Mock rationale: a static list ensures offline operation and deterministic tests.
FORTUNES: List[str] = [
    "You will find great success in unexpected places.",
    "A fresh start will put you on the path to success.",
    "Patience is a virtue; good things come to those who wait.",
    "Adventure awaits you this weekend.",
    "Your hard work will soon pay off.",
]

def get_fortune() -> str:
    """Return a random fortune from the built‑in list.

    The function uses :pyfunc:`random.choice` which can be mocked in tests for
    deterministic behaviour.
    """
    return random.choice(FORTUNES)

if __name__ == "__main__":
    print(get_fortune())
