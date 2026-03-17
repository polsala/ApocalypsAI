import random

ADJECTIVES = [
    "Radiant",
    "Gloomy",
    "Silent",
    "Feral",
    "Eternal",
    "Cursed",
    "Dusty",
    "Howling",
    "Blazing",
    "Shimmering"
]

CREATURES = [
    "Wasteland Wyrm",
    "Dust Devil",
    "Radioactive Rat",
    "Ashen Scavenger",
    "Molten Mantis",
    "Neon Nighthawk",
    "Grim Golem",
    "Spectral Serpent",
    "Void Vulture",
    "Chaos Crawler"
]

def generate_name() -> str:
    """Return a random cryptid name composed of an adjective and a creature."""
    return f"{random.choice(ADJECTIVES)} {random.choice(CREATURES)}"

if __name__ == "__main__":
    print(generate_name())
