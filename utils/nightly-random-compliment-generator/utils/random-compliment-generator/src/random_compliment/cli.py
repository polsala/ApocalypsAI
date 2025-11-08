import argparse
import random
from .core import get_random_compliment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="random-compliment",
        description="Print a random uplifting compliment.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)  # No options yet, but placeholder for future expansion
    print(get_random_compliment())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
