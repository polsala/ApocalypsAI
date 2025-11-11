import random
from typing import List

_FORTUNES: List[str] = [
    "You will find great success in unexpected places.",
    "A fresh start will put you on the path to happiness.",
    "Patience is a virtue; good things come to those who wait.",
    "Adventure awaits you this week.",
    "Your creativity will shine bright today."
]

def get_fortune() -> str:
    """Return a random fortune from the predefined list."""
    return random.choice(_FORTUNES)

def main() -> None:
    """CLI entry point that prints a fortune to stdout."""
    print(get_fortune())

if __name__ == "__main__":
    main()
