import random
import argparse
import sys

def quench_quibble(options: list[str]) -> str:
    """
    Randomly selects one option from a list to quench a quibble.
    """
    if not options:
        raise ValueError("Options list cannot be empty.")
    return random.choice(options)

def main():
    parser = argparse.ArgumentParser(
        description="Quantum Quibble Quencher: Resolve minor disagreements or make trivial decisions by randomly selecting an option."
    )
    parser.add_argument(
        "options",
        nargs="+",
        help="A list of options to choose from (e.g., 'eat beans' 'save beans' 'trade beans')."
    )
    args = parser.parse_args()

    try:
        chosen_option = quench_quibble(args.options)
        print(f"The Quantum Quibble Quencher has spoken! The chosen path is: '{chosen_option}'")
        sys.exit(0)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
