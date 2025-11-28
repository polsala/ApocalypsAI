import random
import sys

def flip_coin():
    """Flips a virtual coin and returns 'Heads' or 'Tails'."""
    return random.choice(["Heads", "Tails"])

def roll_dice(sides=6):
    """
    Rolls a virtual die with the specified number of sides.
    Defaults to a 6-sided die.
    """
    if not isinstance(sides, int) or sides < 1:
        raise ValueError("Number of sides must be a positive integer.")
    return random.randint(1, sides)

def choose_option(options):
    """
    Chooses one option randomly from a list of options.
    """
    if not options:
        raise ValueError("Please provide at least one option to choose from.")
    return random.choice(options)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python src/quencher.py coin")
        print("  python src/quencher.py dice [sides]")
        print("  python src/quencher.py choose <option1> <option2> ...")
        sys.exit(1)

    command = sys.argv[1]

    if command == "coin":
        print(flip_coin())
    elif command == "dice":
        sides = 6
        if len(sys.argv) > 2:
            try:
                sides = int(sys.argv[2])
            except ValueError:
                print("Error: Dice sides must be an integer.", file=sys.stderr)
                sys.exit(1)
        try:
            print(roll_dice(sides))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif command == "choose":
        options = sys.argv[2:]
        if not options:
            print("Error: Please provide options for 'choose'.", file=sys.stderr)
            sys.exit(1)
        try:
            print(choose_option(options))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
