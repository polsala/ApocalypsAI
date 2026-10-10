import random

_TIPS = [
    "Remember to ration your canned beans.",
    "Always keep a spare bottle of water in your backpack.",
    "Never trust a silent mutant.",
    "Solar panels are your best friend on sunny days.",
    "Map your safe zones before nightfall."
]

def get_tip() -> str:
    """Return a random tip."""
    return random.choice(_TIPS)

if __name__ == "__main__":
    print(get_tip())
