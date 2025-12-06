#!/usr/bin/env python3
"""
Random ANSI Art Generator

Selects a random piece of ASCII art with ANSI colour codes from a built‑in collection
and prints it to stdout.
"""

import random
import sys

# ANSI colour codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

ART_COLLECTION = [
    f"{RED}  /\\_/\\  {RESET}\n{RED} ( o.o ) {RESET}\n{RED}  > ^ <  {RESET}",
    f"{GREEN}   _/\\_   {RESET}\n{GREEN}  ( o.o ) {RESET}\n{GREEN}   > ^ <  {RESET}",
    f"{YELLOW}  .-\"\"\"-. {RESET}\n{YELLOW} / .===. \\{RESET}\n{YELLOW} \\/ 6 6 \\/{RESET}\n{YELLOW} ( \\_Y_/ ){RESET}\n{YELLOW}  `-----' {RESET}",
    f"{BLUE}   __   __{RESET}\n{BLUE}  /  \\_/  \\{RESET}\n{BLUE}  \\__/ \\__/ {RESET}",
    f"{MAGENTA}   (\\_/){RESET}\n{MAGENTA}  ( •_•){RESET}\n{MAGENTA}  / >🍪 {RESET}",
]

def get_random_art() -> str:
    """Return a random ANSI‑colored ASCII art string."""
    return random.choice(ART_COLLECTION)

def main() -> None:
    """CLI entry point."""
    art = get_random_art()
    print(art)

if __name__ == "__main__":
    # Ensure deterministic exit code for CI
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
