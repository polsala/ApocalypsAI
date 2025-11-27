#!/usr/bin/env python3
"""Emoji Mood Tracker utility.

Reads lines from a file or stdin and prefixes each line with an emoji that
represents the line's sentiment based on a tiny keyword list.
"""
import argparse
import sys
from typing import List

POSITIVE = {"happy", "joy", "love", "excellent", "good", "great", "wonderful", "fantastic", "awesome"}
NEGATIVE = {"sad", "angry", "hate", "terrible", "bad", "awful", "horrible", "worst"}


def get_mood(line: str) -> str:
    """Return an emoji representing the mood of *line*.

    The function lower‑cases the line, splits on whitespace and checks for the
    presence of any word from the positive or negative sets.
    """
    lowered = line.lower()
    words = set(lowered.split())
    if words & POSITIVE:
        return "😊"
    if words & NEGATIVE:
        return "😞"
    return "😐"


def process_lines(lines: List[str]) -> List[str]:
    """Prefix each line with its mood emoji.

    Trailing newlines are stripped to keep output tidy.
    """
    return [f"{get_mood(line)} {line.rstrip()}" for line in lines]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    parser.add_argument(
        "--file",
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Path to input file (default: stdin)",
    )
    args = parser.parse_args()
    lines = args.file.readlines()
    for out in process_lines(lines):
        print(out)


if __name__ == "__main__":
    main()
