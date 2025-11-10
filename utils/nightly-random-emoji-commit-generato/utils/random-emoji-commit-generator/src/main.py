import argparse
import random
import sys

EMOJIS = [
    "✨",
    "🐛",
    "🚀",
    "🛠️",
    "📦",
    "🔧",
    "⚡",
    "🔥",
    "💡",
    "🎉",
]

def generate_message(message: str) -> str:
    """Return a commit message prefixed with a random emoji."""
    emoji = random.choice(EMOJIS)
    return f"{emoji} {message}"

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a random emoji commit message.")
    parser.add_argument("message", nargs="+", help="Commit message description")
    args = parser.parse_args()
    msg = " ".join(args.message)
    print(generate_message(msg))

if __name__ == "__main__":
    main()
