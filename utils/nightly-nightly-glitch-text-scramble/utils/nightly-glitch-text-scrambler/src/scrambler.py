import random
import sys

def _substitute_char(char, rng):
    """Substitutes a character with a random symbol or similar-looking char."""
    if char.isalpha():
        if rng.random() < 0.5: # 50% chance to substitute with a symbol
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
            return rng.choice(symbols)
        else: # 50% chance to substitute with a visually similar char
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
                'A': '4', 'E': '€', 'I': '!', 'O': 'Ø', 'S': '$', 'T': '+'
            }
            return substitutions.get(char, char)
    elif char.isdigit():
        return rng.choice("0123456789") # Just another digit
    return char

def _insert_char(char, rng):
    """Inserts a random symbol next to a character."""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    return char + rng.choice(symbols)

def scramble_text(text: str, intensity: float = 0.1, seed: int = None) -> str:
    """
    Applies various "glitch" effects to a given text string.

    Args:
        text (str): The input string to scramble.
        intensity (float): A value between 0.0 and 1.0, controlling the
                           degree of scrambling. Higher values mean more glitches.
        seed (int, optional): A seed for the random number generator to ensure
                              deterministic results. Defaults to None.

    Returns:
        str: The glitched text string.
    """
    if not (0.0 <= intensity <= 1.0):
        raise ValueError("Intensity must be between 0.0 and 1.0")

    if not text:
        return ""

    rng = random.Random(seed) # Mock rationale: Using a seeded random number generator ensures deterministic output for tests.

    glitched_chars = []
    for i, char in enumerate(text):
        if rng.random() < intensity:
            glitch_type = rng.random()
            if glitch_type < 0.3: # 30% chance for substitution
                glitched_chars.append(_substitute_char(char, rng))
            elif glitch_type < 0.6: # 30% chance for insertion
                glitched_chars.append(_insert_char(char, rng))
            elif glitch_type < 0.8: # 20% chance for deletion (skip char)
                continue
            else: # 20% chance for case change
                if char.isalpha():
                    glitched_chars.append(char.swapcase())
                else:
                    glitched_chars.append(char)
        else:
            glitched_chars.append(char)

    # Add a small chance for overall text reversal or segment reversal at higher intensities
    if intensity > 0.5 and rng.random() < (intensity - 0.5) * 0.5:
        if rng.random() < 0.5: # Reverse entire string
            return "".join(glitched_chars[::-1])
        else: # Reverse a segment
            start = rng.randint(0, len(glitched_chars) // 2)
            end = rng.randint(len(glitched_chars) // 2, len(glitched_chars))
            segment = glitched_chars[start:end]
            glitched_chars[start:end] = segment[::-1]

    return "".join(glitched_chars)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply glitch effects to text.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("text", type=str, help="The input text to scramble.")
    parser.add_argument("--intensity", type=float, default=0.1,
                        help="Intensity of scrambling (0.0 to 1.0).")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed for random number generator for deterministic results.")

    args = parser.parse_args()

    try:
        glitched_output = scramble_text(args.text, args.intensity, args.seed)
        print(f"Original: {args.text}")
        print(f"Glitched: {glitched_output}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
