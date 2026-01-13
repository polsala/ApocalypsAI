#!/usr/bin/env python3
import random
import sys
import pathlib


def load_quotes(path: pathlib.Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    quotes_file = pathlib.Path(__file__).parent / "quotes.txt"
    quotes = load_quotes(quotes_file)
    if not quotes:
        print("No quotes found.", file=sys.stderr)
        sys.exit(1)
    print(random.choice(quotes))


if __name__ == "__main__":
    main()
