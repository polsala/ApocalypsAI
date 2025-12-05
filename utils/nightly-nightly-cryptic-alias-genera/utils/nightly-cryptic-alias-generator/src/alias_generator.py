import hashlib
import sys

# Whimsical and apocalyptic themed word lists
ADJECTIVES = [
    "Rusty", "Silent", "Whispering", "Cosmic", "Temporal", "Forgotten",
    "Glimmering", "Shadow", "Void", "Ember", "Runic", "Spectral",
    "Iron", "Dusty", "Fading", "Ancient", "Mystic", "Quantum",
    "Echoing", "Stellar", "Grim", "Lost", "Vigilant", "Crystalline"
]

NOUNS = [
    "Oracle", "Echo", "Cipher", "Beacon", "Relic", "Shard",
    "Nexus", "Chronicle", "Glyph", "Sentinel", "Vault", "Whisper",
    "Loom", "Catalyst", "Spire", "Fragment", "Core", "Matrix",
    "Conduit", "Sanctum", "Obelisk", "Vortex", "Guardian", "Key"
]

def generate_alias(input_string: str) -> str:
    """
    Generates a deterministic, two-word cryptic alias for a given input string.

    The alias is formed by combining an adjective and a noun selected from
    predefined lists, based on a SHA256 hash of the input string.
    """
    if not input_string:
        return "Empty Void" # A special alias for empty input

    # Use SHA256 for a strong, deterministic hash
    hash_object = hashlib.sha256(input_string.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)

    # Select adjective and noun using modulo arithmetic on the hash
    adj_index = hash_int % len(ADJECTIVES)
    # Shift the hash to get a different part for the noun, ensuring better distribution
    noun_index = (hash_int >> 8) % len(NOUNS) # Shift by 8 bits to use a different part of the hash

    adjective = ADJECTIVES[adj_index]
    noun = NOUNS[noun_index]

    return f"{adjective} {noun}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/alias_generator.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    alias = generate_alias(input_string)
    print(alias)

if __name__ == "__main__":
    main()
