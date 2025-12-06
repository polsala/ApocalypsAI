#!/usr/bin/env python3
"""Random Commit Message generator.

When executed, prints a whimsical commit message such as:
    🚀 Add shiny pipeline
"""
import random
import sys

EMOJIS = ["✨", "🚀", "🐛", "🔧", "📦"]
ADJECTIVES = ["quick", "mysterious", "robust", "elegant", "shiny"]
VERBS = ["add", "fix", "refactor", "remove", "update"]
NOUNS = ["widget", "module", "feature", "bug", "pipeline"]

def generate_message() -> str:
    """Return a random commit message in the form:
    <emoji> <Verb> <adjective> <noun>
    """
    emoji = random.choice(EMOJIS)
    verb = random.choice(VERBS).capitalize()
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{emoji} {verb} {adjective} {noun}"

def main() -> None:
    print(generate_message())

if __name__ == "__main__":
    sys.exit(main())
