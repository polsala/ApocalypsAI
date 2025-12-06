import random
import string
import argparse

# Mock rationale: For deterministic testing, we'll mock random.choice and random.sample.
# For the actual utility, we use the real random module.

APOCALYPSE_WORDS = [
    "wasteland", "bunker", "fallout", "mutant", "scavenger", "survival",
    "radiant", "doomsday", "outpost", "nomad", "ruins", "sanctuary",
    "desolate", "apocalypse", "reactor", "anomaly", "fortress", "relic",
    "marauder", "cataclysm", "epoch", "genesis", "horizon", "solstice",
    "vanguard", "zephyr", "cryptic", "dystopia", "ember", "fissure",
    "gloom", "havoc", "inferno", "juggernaut", "krypton", "lunar",
    "maelstrom", "nebula", "oblivion", "phantom", "quarantine", "ravage",
    "shroud", "typhoon", "umbra", "vortex", "wraith", "xenon", "yonder", "zenith"
]

def generate_random_password(
    length: int = 12,
    include_digits: bool = True,
    include_symbols: bool = True,
    include_uppercase: bool = True,
    include_lowercase: bool = True
) -> str:
    """
    Generates a strong, random password.
    """
    if length <= 0:
        raise ValueError("Password length must be positive.")

    characters = ""
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_apocalypse_passphrase(num_words: int = 4, separator: str = "-") -> str:
    """
    Generates a memorable passphrase using a list of apocalypse-themed words.
    """
    if num_words <= 0:
        raise ValueError("Number of words must be positive.")
    if num_words > len(APOCALYPSE_WORDS):
        # Allow repetition if more words than available unique words are requested
        selected_words = [random.choice(APOCALYPSE_WORDS) for _ in range(num_words)]
    else:
        selected_words = random.sample(APOCALYPSE_WORDS, num_words)
    
    return separator.join(selected_words)

def main():
    parser = argparse.ArgumentParser(
        description="Generate strong passwords or apocalypse-themed passphrases."
    )
    parser.add_argument(
        "--mode",
        choices=["random", "passphrase"],
        required=True,
        help="Mode of generation: 'random' for strong passwords, 'passphrase' for themed passphrases."
    )

    # Random password arguments
    parser.add_argument(
        "--length",
        type=int,
        default=12,
        help="Length of the random password (default: 12)."
    )
    parser.add_argument(
        "--digits",
        action="store_true",
        help="Include digits (0-9) in random password."
    )
    parser.add_argument(
        "--symbols",
        action="store_true",
        help="Include symbols (!@#$...) in random password."
    )
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Include uppercase letters (A-Z) in random password."
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Include lowercase letters (a-z) in random password."
    )

    # Passphrase arguments
    parser.add_argument(
        "--words",
        type=int,
        default=4,
        help="Number of words in the passphrase (default: 4)."
    )
    parser.add_argument(
        "--separator",
        type=str,
        default="-",
        help="Separator character for passphrase words (default: '-')."
    )

    args = parser.parse_args()

    if args.mode == "random":
        # If no character types are specified, include all by default
        if not (args.digits or args.symbols or args.uppercase or args.lowercase):
            password = generate_random_password(
                args.length,
                include_digits=True,
                include_symbols=True,
                include_uppercase=True,
                include_lowercase=True
            )
        else:
            password = generate_random_password(
                args.length,
                include_digits=args.digits,
                include_symbols=args.symbols,
                include_uppercase=args.uppercase,
                include_lowercase=args.lowercase
            )
        print(password)
    elif args.mode == "passphrase":
        passphrase = generate_apocalypse_passphrase(args.words, args.separator)
        print(passphrase)

if __name__ == "__main__":
    main()
