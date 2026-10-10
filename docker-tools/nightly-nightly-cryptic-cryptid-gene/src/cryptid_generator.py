import random

_ADJECTIVES = [
    "Neon-Scaled", "Shadowy", "Gigantic", "Miniature", "Ethereal",
    "Flaming", "Glacial", "Thunderous", "Invisible", "Radiant"
]

_CREATURES = [
    "Skywhale", "Mirewolf", "Stonebeetle", "Luminox", "Abyssal Serpent",
    "Crystaline Owl", "Molten Tortoise", "Silk Spider", "Obsidian Panther", "Celestial Fox"
]

_HABITATS = [
    "the moonlit marshes", "the volcanic canyons", "the crystal caves",
    "the endless deserts", "the misty forests", "the stormy seas",
    "the floating islands", "the underground rivers", "the ancient ruins", "the aurora-lit tundra"
]

_BEHAVIORS = [
    "sings lullabies to wandering travelers",
    "guards hidden treasure",
    "weaves dreams into reality",
    "collects lost memories",
    "illuminates the night with bioluminescent breath",
    "creates mirages to confuse predators",
    "dances with the wind",
    "writes poetry in the sand",
    "plays chess with the stars",
    "whispers secrets of the cosmos"
]

def generate() -> str:
    """Return a whimsical cryptid description."""
    name = f"The {random.choice(_ADJECTIVES)} {random.choice(_CREATURES)}"
    habitat = random.choice(_HABITATS)
    behavior = random.choice(_BEHAVIORS)
    return f"{name}, a mysterious creature that dwells in {habitat} and {behavior}."
