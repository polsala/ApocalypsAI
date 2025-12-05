import argparse
import random
import sys


def generate_palette(count: int, seed: int | None = None) -> list[str]:
    """Return a list of *count* random hex color strings.

    If *seed* is provided the randomness is deterministic.
    """
    if count < 0:
        raise ValueError("count must be non‑negative")
    rnd = random.Random(seed)
    return [f"#{rnd.randint(0, 0xFFFFFF):06X}" for _ in range(count)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a hex color palette")
    parser.add_argument("count", type=int, help="Number of colors to generate")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()
    try:
        palette = generate_palette(args.count, args.seed)
        for color in palette:
            print(color)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
