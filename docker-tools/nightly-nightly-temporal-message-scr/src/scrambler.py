import time
import random
import sys
import argparse

def scramble_char(char, level, rng):
    if level == 0:
        return char
    elif level == 1:
        # Moderate: random case change, or minor symbol replacement
        if char.isalpha() and rng.random() < 0.3:
            return char.swapcase()
        elif char.isspace():
            return char
        elif rng.random() < 0.1:
            return rng.choice(['!', '@', '#', '$', '%', '^', '&', '*'])
        return char
    elif level == 2:
        # Aggressive: more frequent case change, symbol replacement, or swap
        if char.isalpha() and rng.random() < 0.5:
            return char.swapcase()
        elif char.isspace():
            return char
        elif rng.random() < 0.3:
            return rng.choice(['!', '@', '#', '$', '%', '^', '&', '*', '?', '~', '+', '-'])
        elif rng.random() < 0.2: # Swap with a random char from a small set
            return rng.choice(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
        return char
    return char

def scramble_message(message, char_scramble_level, word_reorder_level, rng):
    # Apply word reordering first
    words = message.split()
    if word_reorder_level == 1 and len(words) > 1:
        for i in range(len(words) - 1):
            if rng.random() < 0.2: # 20% chance to swap adjacent words
                words[i], words[i+1] = words[i+1], words[i]
    reordered_message = " ".join(words)

    # Apply character scrambling
    scrambled_chars = [scramble_char(c, char_scramble_level, rng) for c in reordered_message]
    return "".join(scrambled_chars)

def main():
    parser = argparse.ArgumentParser(description="A utility to simulate temporal distortion and data corruption on messages.")
    parser.add_argument("message", type=str, help="The input string to be scrambled.")
    parser.add_argument("--delay", type=float, default=0.5, help="The delay in seconds before processing.")
    parser.add_argument("--char-scramble-level", type=int, default=1, choices=[0, 1, 2], help="Level of character scrambling (0-2).")
    parser.add_argument("--word-reorder-level", type=int, default=0, choices=[0, 1], help="Level of word reordering (0-1).")
    parser.add_argument("--seed", type=int, help="Seed for the random number generator for deterministic scrambling.")

    args = parser.parse_args()

    # Create a local random number generator for this instance
    # This ensures that if random.seed() is called, it affects only this instance's operations
    # and not global random state if this were part of a larger system.
    rng = random.Random(args.seed) if args.seed is not None else random.Random()

    # Simulate temporal delay
    time.sleep(args.delay)

    # Scramble the message
    scrambled_output = scramble_message(args.message, args.char_scramble_level, args.word_reorder_level, rng)

    print(scrambled_output)

if __name__ == "__main__":
    main()
