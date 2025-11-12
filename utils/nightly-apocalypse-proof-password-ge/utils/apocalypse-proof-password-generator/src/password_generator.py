import secrets
import argparse

# Whimsical word lists for password generation
ADJECTIVES = [
    "Ancient", "Cosmic", "Silent", "Fiery", "Mystic", "Quantum", "Forgotten",
    "Glimmering", "Shadowy", "Vast", "Ethereal", "Whispering", "Stellar",
    "Runic", "Obsidian", "Crimson", "Emerald", "Golden", "Silver", "Iron"
]

NOUNS = [
    "Relic", "Comet", "Whisper", "Dust", "Echo", "Portal", "Cipher",
    "Glyph", "Nexus", "Vortex", "Shard", "Chronicle", "Beacon",
    "Sentinel", "Obelisk", "Phoenix", "Dragon", "Kraken", "Golem", "Titan"
]

SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=']

def generate_apocalypse_password(
    num_digits: int = 2,
    num_symbols: int = 1
) -> str:
    """
    Generates an apocalypse-proof password with a structured pattern:
    ADJECTIVE-NOUN-DIGITS-SYMBOL-ADJECTIVE-NOUN.
    """
    if num_digits < 1:
        raise ValueError("Number of digits must be at least 1.")
    if num_symbols < 1:
        raise ValueError("Number of symbols must be at least 1.")

    password_parts = [
        secrets.choice(ADJECTIVES),
        secrets.choice(NOUNS),
        ''.join(str(secrets.randbelow(10)) for _ in range(num_digits)), # Digits
        secrets.choice(SYMBOLS),
        secrets.choice(ADJECTIVES),
        secrets.choice(NOUNS)
    ]

    return '-'.join(password_parts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an apocalypse-proof password."
    )
    parser.add_argument(
        "--num-digits",
        type=int,
        default=2,
        help="Number of digits to include in the password (default: 2, min: 1)."
    )
    parser.add_argument(
        "--num-symbols",
        type=int,
        default=1,
        help="Number of symbols to include in the password (default: 1, min: 1)."
    )

    args = parser.parse_args()

    try:
        password = generate_apocalypse_password(
            num_digits=args.num_digits,
            num_symbols=args.num_symbols
        )
        print(f"Your Apocalypse-Proof Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")
