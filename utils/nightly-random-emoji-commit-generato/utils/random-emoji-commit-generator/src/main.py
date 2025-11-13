#!/usr/bin/env python3
"""
Random Emoji Commit Generator

Generates a commit message consisting of random emojis followed by a short action phrase.
"""

import argparse
import random
import sys
from pathlib import Path

EMOJIS = [
    "✨", "🚀", "🐛", "🔧", "🧹", "📦", "⚡", "🔥", "💡", "🛠️",
    "✅", "🔀", "🧪", "📈", "🗑️", "🧹", "🔒", "🧱", "🧩", "🪄"
]

PHRASES = [
    "Refactor code",
    "Fix bug",
    "Add feature",
    "Update docs",
    "Improve performance",
    "Remove deprecated code",
    "Add tests",
    "Upgrade dependencies",
    "Reformat code",
    "Merge branch"
]

def generate_message(num_emojis: int = 2) -> str:
    """Generate a commit message with `num_emojis` random emojis and a random phrase."""
    if num_emojis < 1:
        raise ValueError("num_emojis must be >= 1")
    chosen_emojis = random.sample(EMOJIS, k=num_emojis)
    phrase = random.choice(PHRASES)
    return f"{''.join(chosen_emojis)} {phrase}"

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a whimsical commit message with random emojis."
    )
    parser.add_argument(
        "--num-emojis",
        type=int,
        default=2,
        help="Number of emojis to prepend (default: 2)",
    )
    return parser.parse_args(argv)

def main():
    args = parse_args()
    try:
        message = generate_message(num_emojis=args.num_emojis)
        print(message)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
