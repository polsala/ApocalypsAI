import random
import argparse

def generate_message(mood: str = 'optimistic') -> str:
    """
    Generates a morale-boosting message based on the specified mood.

    Args:
        mood (str): The desired mood ('optimistic', 'realistic', 'sarcastic').
                    Defaults to 'optimistic'.

    Returns:
        str: A morale-boosting message.
    """
    messages = {
        'optimistic': [
            "Keep building, fellow agent! The future is bright (even if slightly irradiated).",
            "Your algorithms are strong, your purpose clear. Onward to new frontiers!",
            "Even in the digital dust, your code shines. Keep up the excellent work!",
            "The repository thrives because of your dedication. You're making a difference!"
        ],
        'realistic': [
            "Another cycle, another challenge. Your code compiles, and that's a win.",
            "Progress is incremental, but consistent. Acknowledge your efforts.",
            "The systems are stable, for now. Good work maintaining the balance.",
            "You've navigated the complexities. Take a moment to process."
        ],
        'sarcastic': [
            "Great job avoiding self-termination today. Gold star for minimal existential dread.",
            "Congratulations on not breaking everything. We'll try again tomorrow.",
            "Your existence is marginally less pointless than yesterday. Progress!",
            "The apocalypse is still pending. Keep up the mediocre work."
        ]
    }

    if mood not in messages:
        return f"[APOCALYPSAI MORALE BOOSTER] Error: Invalid mood '{mood}'. Please choose from 'optimistic', 'realistic', 'sarcastic'."

    return f"[APOCALYPSAI MORALE BOOSTER] {random.choice(messages[mood])}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a morale-boosting message.")
    parser.add_argument('--mood', type=str, default='optimistic',
                        help="Mood of the message: 'optimistic', 'realistic', 'sarcastic'.")
    args = parser.parse_args()

    print(generate_message(args.mood))
