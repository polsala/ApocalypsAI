import random
import os

# Default wordlist for a whimsical touch
DEFAULT_WORDLIST = [
    "apocalypse", "wasteland", "mutant", "scavenger", "rubble",
    "survival", "bunker", "radiation", "echo", "quantum",
    "quirk", "anomaly", "glitch", "signal", "whisper",
    "chronicle", "gloom", "reactor", "cipher", "beacon"
]

def generate_passphrase(num_words: int = 4, separator: str = "-", wordlist: list = None) -> str:
    """
    Generates a secure and memorable passphrase using a list of words.

    Args:
        num_words (int): The number of words to include in the passphrase.
                         Must be between 3 and 10.
        separator (str): The character(s) to use between words.
        wordlist (list, optional): A custom list of words to draw from.
                                   If None, uses a default apocalyptic-themed list.

    Returns:
        str: The generated passphrase.

    Raises:
        ValueError: If num_words is out of range or wordlist is too small.
    """
    if not (3 <= num_words <= 10):
        raise ValueError("Number of words must be between 3 and 10.")

    words_to_use = wordlist if wordlist is not None else DEFAULT_WORDLIST

    if len(words_to_use) < num_words:
        raise ValueError(f"Wordlist must contain at least {num_words} unique words.")

    # Use SystemRandom for cryptographically secure randomness
    rng = random.SystemRandom()
    selected_words = rng.sample(words_to_use, num_words)

    return separator.join(selected_words)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a secure and memorable passphrase."
    )
    parser.add_argument(
        "-n", "--num-words", type=int, default=4,
        help="Number of words in the passphrase (3-10)."
    )
    parser.add_argument(
        "-s", "--separator", type=str, default="-",
        help="Separator character(s) between words."
    )
    parser.add_argument(
        "-w", "--wordlist-file", type=str,
        help="Path to a custom wordlist file (one word per line)."
    )

    args = parser.parse_args()

    custom_wordlist = None
    if args.wordlist_file:
        if not os.path.exists(args.wordlist_file):
            print(f"Error: Wordlist file '{args.wordlist_file}' not found.", file=os.stderr)
            exit(1)
        with open(args.wordlist_file, 'r') as f:
            custom_wordlist = [line.strip() for line in f if line.strip()]

    try:
        passphrase = generate_passphrase(
            num_words=args.num_words,
            separator=args.separator,
            wordlist=custom_wordlist
        )
        print(passphrase)
    except ValueError as e:
        print(f"Error: {e}", file=os.stderr)
        exit(1)

if __name__ == "__main__":
    main()
