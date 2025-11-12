import argparse
import sys
from typing import List

# A small built‑in word list for demonstration purposes.
# In real usage you can replace this with a full dictionary.
WORDLIST = [
    "apple",
    "apply",
    "ample",
    "crane",
    "slate",
    "flame",
    "blame",
    "grape",
    "pride",
]

def filter_words(guess: str, pattern: str, wordlist: List[str]) -> List[str]:
    """Return words that satisfy the guess/pattern constraints.

    Parameters
    ----------
    guess: str
        The guessed word (5 letters).
    pattern: str
        Feedback string composed of 'g', 'y', 'b'.
    wordlist: List[str]
        Candidate words.
    """
    guess = guess.lower()
    pattern = pattern.lower()
    if len(guess) != 5 or len(pattern) != 5:
        raise ValueError("Both guess and pattern must be exactly 5 characters long.")

    result = []
    for word in wordlist:
        word = word.lower()
        if len(word) != 5:
            continue
        ok = True
        for i, (g_char, p_char) in enumerate(zip(guess, pattern)):
            w_char = word[i]
            if p_char == "g":
                if w_char != g_char:
                    ok = False
                    break
            elif p_char == "y":
                if g_char == w_char or g_char not in word:
                    ok = False
                    break
            elif p_char == "b":
                if g_char in word:
                    ok = False
                    break
            else:
                raise ValueError("Pattern must contain only 'g', 'y', or 'b'.")
        if ok:
            result.append(word)
    return result

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wordle helper – filter possible solutions.")
    parser.add_argument("--guess", required=True, help="Your guessed word (5 letters)")
    parser.add_argument("--pattern", required=True, help="Feedback pattern (e.g., ggybb)")
    args = parser.parse_args(argv)

    try:
        candidates = filter_words(args.guess, args.pattern, WORDLIST)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if candidates:
        for cand in candidates:
            print(cand)
    else:
        print("No matching words found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
