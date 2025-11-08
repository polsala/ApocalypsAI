"""
CLI entry point for the Daily Zen Quote Generator.
"""

from .quote import get_quote

def main() -> None:
    """Print today's quote to stdout."""
    print(get_quote())

if __name__ == "__main__":
    main()
