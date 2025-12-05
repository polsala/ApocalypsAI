import random

ADJECTIVES = [
    "Wasteland", "Rusty", "Feral", "Shadow", "Silent", "Dusty", "Grim",
    "Broken", "Scorched", "Whispering", "Forgotten", "Mutant", "Quantum", "Echoing",
    "Desolate", "Barren", "Shattered", "Bleak", "Stark", "Cryptic", "Spectral"
]

NOUNS = [
    "Nomad", "Scavenger", "Relic", "Beacon", "Whisper", "Shard", "Vault",
    "Drifter", "Chronicle", "Nexus", "Anomaly", "Cipher", "Glyph", "Rubble",
    "Outpost", "Sanctuary", "Echo", "Mirage", "Vortex", "Sentinel", "Catalyst"
]

def generate_codename():
    """
    Generates a whimsical, apocalypse-themed codename by combining a random adjective and noun.
    The format is 'Adjective-Noun'.
    """
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{adjective}-{noun}"

if __name__ == "__main__":
    print(f"Generated Codename: {generate_codename()}")
