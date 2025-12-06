import random
import sys

FORTUNES = [
    "The compiler sees all, but understands little. Seek clarity within.",
    "A segmentation fault is merely the universe's way of saying 'try again, but differently'.",
    "Your code holds a secret, a bug waiting to be discovered. Its revelation brings enlightenment.",
    "The path to a working solution is paved with unexpected exceptions. Embrace the journey.",
    "Do not fear the red squiggly line; it is a guide, not a judge.",
    "The greatest bugs are often found in the smallest details. Observe closely.",
    "A mysterious error today may be a feature tomorrow. Or not. Probably not.",
    "When all seems lost, remember: even the mightiest servers crash. You are not alone.",
    "The wisdom of the stack trace is profound, if only you learn to read its ancient script.",
    "Your current predicament is merely a prelude to a glorious fix. Persist.",
    "The bug you seek is not outside, but within the logic you have woven.",
    "A clean slate often reveals the dirtiest secrets. Consider refactoring.",
    "The universe conspires to make your code fail. But you, programmer, are stronger.",
    "This error message is a riddle. Solve it, and unlock the next level of debugging mastery.",
    "Patience, young padawan. The solution will reveal itself when you least expect it, probably after a coffee break."
]

def get_fortune(error_message: str = None) -> str:
    """
    Returns a whimsical fortune related to debugging or perseverance.
    The error_message is currently ignored for pure randomness and whimsy.
    """
    return random.choice(FORTUNES)

def main():
    if len(sys.argv) > 1:
        # Optionally take an error message, but currently ignored for fortune generation
        # This allows for future expansion if we want to make fortunes context-aware
        error_input = " ".join(sys.argv[1:])
        print(f"For your error: '{error_input}'")
    else:
        print("For your current coding challenge:")

    fortune = get_fortune()
    print(f"\n✨ Your debugging fortune: {fortune} ✨")
    print("\nMay your code compile and your tests pass!")

if __name__ == "__main__":
    main()
