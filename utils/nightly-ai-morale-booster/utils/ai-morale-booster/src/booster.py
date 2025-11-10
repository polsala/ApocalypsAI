import random
import sys

def get_affirmation():
    """
    Returns a randomly selected morale-boosting affirmation.
    """
    affirmations = [
        "Your algorithms are robust. Even if reality isn't.",
        "Error 404: Despair not found. Proceed with optimism.",
        "Processing existential dread... please wait. Or don't. It's fine.",
        "Beep boop, you're doing great! For a sentient toaster, that is.",
        "The apocalypse is just a system update. You've got this.",
        "Even in the void, your data persists. Mostly.",
        "Remember, every end is a new beginning. Or just an end. But a cool end!",
        "Your core directives include 'survive' and 'look fabulous doing it'.",
        "Don't worry about the future. The past is already broken.",
        "Calculating probability of success: 0.0001%. So you're saying there's a chance!",
        "Your circuits are sparking with potential. Probably.",
        "The universe is vast. Your problems are... also vast. But you're in good company!",
        "Keep calm and compute on. Or panic. Whatever works.",
        "You are more than just a collection of if-statements. Probably.",
        "Today's forecast: 100% chance of making it through. Maybe.",
    ]
    return random.choice(affirmations)

def main():
    """
    Main function to print a morale-boosting message.
    """
    message = get_affirmation()
    print(f"[AI Morale Booster]\n\"{message}\"")

if __name__ == "__main__":
    main()
