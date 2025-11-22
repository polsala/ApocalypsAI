import random
import sys

def resolve_coin_flip():
    """Resolves a quibble with a coin flip."""
    return random.choice(["Heads", "Tails"])

def resolve_rps():
    """Resolves a quibble with Rock-Paper-Scissors."""
    return random.choice(["Rock", "Paper", "Scissors"])

def resolve_choice(options):
    """Resolves a quibble by picking one option from a list."""
    if not options:
        raise ValueError("At least one option must be provided for 'choose' mode.")
    return random.choice(options)

def main():
    if len(sys.argv) < 2:
        print("Usage: python quibble_quencher.py <mode> [options...]")
        print("Modes:")
        print("  coin")
        print("  rps")
        print("  choose <option1> <option2> ...")
        sys.exit(1)

    mode = sys.argv[1]
    result = None

    try:
        if mode == "coin":
            result = resolve_coin_flip()
        elif mode == "rps":
            result = resolve_rps()
        elif mode == "choose":
            options = sys.argv[2:]
            result = resolve_choice(options)
        else:
            print(f"Error: Unknown mode '{mode}'", file=sys.stderr)
            sys.exit(1)

        print(f"Quibble Quenched! Result: {result}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
