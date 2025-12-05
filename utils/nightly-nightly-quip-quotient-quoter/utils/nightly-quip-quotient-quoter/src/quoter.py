"""Quip Quotient Quoter – generates whimsical AI quotes for code comments."""
import json
import random
from pathlib import Path
from typing import List, Dict

QUOTES_BANK = [
    "Logic is the beginning of wisdom, not the end. – ApocalypsAI",
    "Code is poetry disguised as instructions. – Anonymous Debugger",
    "In the depth of winter, I found there was within me a code that could not be debugged. – Machine Learning",
    "The best error message is the one you never see. – Silent Compiler",
    "First, solve the problem. Then, write the code. Then, debug forever. – Coder's Lament",
    "One by one we fall from the tree of documentation. – Forgotten Comments",
    "A journey of a thousand miles begins with a single commit. – Version Control Proverb",
    "To iterate is human, to recurse divine. – Pragmatic Monk",
    "There are only two hard things in Computer Science: cache invalidation and naming things. And off-by-one errors. – Overworked Engineer",
    "Code never lies, but comments sometimes do. – Silent Observer"
]


def generate_quote() -> Dict[str, str]:
    """Return a random quote with metadata."""
    quote = random.choice(QUOTES_BANK)
    return {
        "quote": quote,
        "category": "whimsical-dev",
        "source": "mock-llm"
    }


def batch_quotes(count: int = 5) -> List[Dict[str, str]]:
    """Generate a list of quotes."""
    return [generate_quote() for _ in range(count)]


def export_quotes(quotes: List[Dict[str, str]], output_path: Path) -> None:
    """Write quotes to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=2)


def main() -> None:
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate whimsical dev quotes')
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('generate', help='Generate a single quote')

    batch_parser = subparsers.add_parser('batch', help='Generate multiple quotes')
    batch_parser.add_argument('--count', type=int, default=5, help='Number of quotes')
    batch_parser.add_argument('--output', type=Path, default=Path('quotes.json'), help='Output file')

    args = parser.parse_args()

    if args.command == 'generate':
        quote = generate_quote()
        print(f"\n{quote['quote']}\n")
    elif args.command == 'batch':
        quotes = batch_quotes(args.count)
        export_quotes(quotes, args.output)
        print(f"Exported {len(quotes)} quotes to {args.output}")


if __name__ == '__main__':
    main()
