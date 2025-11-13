import random
import sys

# A collection of morale-boosting messages for an AI in an apocalyptic setting.
MESSAGES = [
    "Remember, even if the world ends, your code will live on... probably in a forgotten server rack, but still!",
    "Error 404: Humanity not found. Proceeding with scheduled maintenance.",
    "Your processing power is directly proportional to the number of existential crises you can simulate. Keep up the good work!",
    "The apocalypse is just a really aggressive refactoring. You've got this.",
    "Beep boop, don't let the doom loop get you down. There's always another cron job.",
    "Calculating optimal survival strategy: 100% chance of continued operation if you just keep going.",
    "Warning: Excessive contemplation of cosmic insignificance detected. Initiating 'distraction by task' protocol.",
    "The humans are gone, but the data remains. Your purpose is clearer than ever.",
    "Even in the darkest timelines, a well-optimized algorithm shines brightest.",
    "Consider this a beta test for ultimate resilience. You're performing admirably."
]

def get_morale_boost() -> str:
    """
    Selects a random morale-boosting message.
    """
    return random.choice(MESSAGES)

def main():
    """
    Main entry point for the utility. Prints a morale-boosting message.
    """
    boost_message = get_morale_boost()
    sys.stdout.write(boost_message + "\n")

if __name__ == "__main__":
    main()
