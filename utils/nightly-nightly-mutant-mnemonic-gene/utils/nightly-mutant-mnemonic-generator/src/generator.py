import argparse
import os
import secrets
import random
import sys

# Path to the word list file relative to this script
WORD_LIST_PATH = os.path.join(os.path.dirname(__file__), 'words.txt')

def load_word_list(path: str) -> list[str]:
    """Loads words from a file, one word per line."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        if not words:
            raise ValueError(f"Word list '{path}' is empty.")
        return words
    except FileNotFoundError:
        raise FileNotFoundError(f"Word list file not found at '{path}'.")
    except Exception as e:
        raise IOError(f"Error loading word list from '{path}': {e}")

def generate_mnemonic(
    num_words: int,
    separator: str,
    word_list: list[str],
    seed: int = None
) -> str:
    """
    Generates a mnemonic passphrase from the given word list.

    Args:
        num_words: The number of words to include in the passphrase.
        separator: The string to use to join the words.
        word_list: A list of words to choose from.
        seed: An optional integer seed for deterministic generation (for testing).
              If None, uses cryptographically secure randomness.

    Returns:
        A string representing the generated mnemonic passphrase.

    Raises:
        ValueError: If num_words is not positive or is greater than the available unique words.
    """
    if num_words <= 0:
        raise ValueError("Number of words must be positive.")
    if num_words > len(word_list):
        raise ValueError(
            f"Cannot generate {num_words} unique words from a list of only "
            f"{len(word_list)} words."
        )

    chosen_words = []
    available_words = list(word_list) # Create a mutable copy to ensure uniqueness

    if seed is not None:
        # Mock rationale: Using a seeded random for deterministic testing.
        # For actual security, secrets.choice is used.
        rng = random.Random(seed)
        choice_func = rng.choice
    else:
        # Mock rationale: secrets.choice is cryptographically secure for production.
        # No mocking needed here as it's the intended production path.
        choice_func = secrets.choice

    for _ in range(num_words):
        if not available_words:
            # This should ideally be caught by the num_words > len(word_list) check,
            # but as a safeguard for unexpected empty list during iteration.
            break
        word = choice_func(available_words)
        chosen_words.append(word)
        available_words.remove(word) # Ensure uniqueness by removing chosen word

    return separator.join(chosen_words)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a memorable passphrase from a post-apocalyptic word list."
    )
    parser.add_argument(
        "--words",
        type=int,
        default=4,
        help="The number of words to include in the passphrase (default: 4)",
    )
    parser.add_argument(
        "--separator",
        type=str,
        default="-",
        help="The character(s) to use between words (default: '-')",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="(Optional) A numeric seed for deterministic generation. DO NOT USE FOR ACTUAL SECURITY; ONLY FOR TESTING.",
    )

    args = parser.parse_args()

    try:
        words = load_word_list(WORD_LIST_PATH)
        mnemonic = generate_mnemonic(
            args.words, args.separator, words, seed=args.seed
        )
        print(mnemonic)
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
