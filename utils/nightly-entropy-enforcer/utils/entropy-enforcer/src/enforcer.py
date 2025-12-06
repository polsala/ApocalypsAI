import argparse
import string
import secrets
import sys

def generate_string(length: int,
                    include_digits: bool = True,
                    include_lower: bool = True,
                    include_upper: bool = True,
                    include_symbols: bool = False,
                    exclude_ambiguous: bool = False) -> str:
    """Generates a random string with specified characteristics."""
    character_pool = []
    if include_digits:
        character_pool.extend(string.digits)
    if include_lower:
        character_pool.extend(string.ascii_lowercase)
    if include_upper:
        character_pool.extend(string.ascii_uppercase)
    if include_symbols:
        character_pool.extend(string.punctuation)

    if not character_pool:
        raise ValueError("At least one character type must be included.")

    if exclude_ambiguous:
        # Common ambiguous characters that can be confused visually
        ambiguous_chars = "lIO01"
        # Filter the pool
        character_pool = [c for c in character_pool if c not in ambiguous_chars]

    if not character_pool:
        raise ValueError("Character pool became empty after excluding ambiguous characters. Adjust character type selections.")

    return ''.join(secrets.choice(character_pool) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(
        description="Generate high-entropy random strings (passwords, API keys, tokens)."
    )
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="Length of the generated string.")
    parser.add_argument("--no-digits", action="store_false", dest="include_digits",
                        help="Exclude digits (0-9).")
    parser.add_argument("--no-lower", action="store_false", dest="include_lower",
                        help="Exclude lowercase letters (a-z).")
    parser.add_argument("--no-upper", action="store_false", dest="include_upper",
                        help="Exclude uppercase letters (A-Z).")
    parser.add_argument("-s", "--symbols", action="store_true", dest="include_symbols",
                        help="Include symbols (!@#$%...)."
    )
    parser.add_argument("-x", "--exclude-ambiguous", action="store_true",
                        help="Exclude ambiguous characters (e.g., l, I, O, 0, 1).")

    args = parser.parse_args()

    try:
        generated_string = generate_string(
            length=args.length,
            include_digits=args.include_digits,
            include_lower=args.include_lower,
            include_upper=args.include_upper,
            include_symbols=args.include_symbols,
            exclude_ambiguous=args.exclude_ambiguous
        )
        print(generated_string)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
