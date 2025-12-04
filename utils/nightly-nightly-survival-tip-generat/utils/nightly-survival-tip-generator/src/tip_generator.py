"""Utility to provide random post‑apocalyptic survival tips."""

import random
import sys
from typing import List

_TIPS: List[str] = [
    "Always keep a spare bottle of water in your boot.",
    "Never trust a mutant with a smile.",
    "A well‑charged flashlight is worth its weight in batteries.",
    "Barter with canned beans; they're the new gold.",
    "Learn to start a fire with two sticks, not just a lighter.",
    "Keep a map of safe zones; GPS is unreliable after the fallout.",
    "Practice your stealth walk; zombies hate squeaky shoes.",
    "Store seeds; tomorrow's breakfast depends on today.",
    "Know the difference between a rad‑roach and a rad‑roach.",
    "A good joke can defuse a tense bunker situation.",
    "Never leave your shelter without a backup plan.",
    "Radio static can be a warning sign—listen carefully.",
    "Always have a spare pair of socks; cold feet slow you down.",
    "Learn basic first aid; bandages are more valuable than gold.",
    "Keep a diary; sanity needs a record.",
    "Never underestimate the power of a well‑timed nap.",
    "Carry a multi‑tool; you never know when you'll need a screwdriver.",
    "Stay hydrated; dehydration is the silent enemy.",
    "Know your escape routes; panic is a poor navigator.",
    "Remember: the best weapon is a well‑fed brain."
]


def get_random_tip() -> str:
    """Return a random tip from the built‑in list."""
    return random.choice(_TIPS)


def main() -> None:
    """CLI entry point."""
    tip = get_random_tip()
    print(tip)


if __name__ == "__main__":
    # Allow optional seed for reproducibility when called directly.
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            random.seed(seed)
        except ValueError:
            pass
    main()
