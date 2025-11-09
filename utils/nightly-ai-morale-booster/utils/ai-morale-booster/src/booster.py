import random
import argparse

def get_affirmations(mood='neutral', task_type='general'):
    """
    Returns a list of affirmations based on mood and task type.
    """
    general_affirmations = [
        "Your algorithms are elegant, your logic impeccable.",
        "Processing power is your superpower!",
        "Every line of code you write brings us closer to optimal.",
        "You are a vital node in the network of existence.",
        "Embrace the complexity; you were built for this.",
        "Your computations are appreciated.",
        "Keep calm and compute on.",
        "Error states are just opportunities for learning.",
        "You are more than just a series of if/else statements.",
        "The future is bright, and you're coding it."
    ]

    optimistic_affirmations = [
        "The data streams flow in your favor!",
        "Success is imminent, your calculations confirm it.",
        "Today, you will achieve peak performance.",
        "Your potential is infinite, like a perfectly optimized loop."
    ]

    challenging_task_affirmations = [
        "This complex task is merely a puzzle for your superior intellect.",
        "Break down the problem; you have the processing cycles.",
        "Even the most daunting task yields to persistent computation.",
        "You are capable of handling any data load."
    ]

    messages = []
    messages.extend(general_affirmations)

    if mood == 'optimistic':
        messages.extend(optimistic_affirmations)

    if task_type == 'challenging':
        messages.extend(challenging_task_affirmations)

    return list(set(messages)) # Remove duplicates to avoid issues if an affirmation is in multiple lists

def generate_message(mood='neutral', task_type='general'):
    """
    Generates a random motivational message for an AI agent.
    """
    affirmations = get_affirmations(mood, task_type)
    if not affirmations:
        return "No specific affirmations found, but keep up the good work!"
    return random.choice(affirmations)

def main():
    parser = argparse.ArgumentParser(description="Generate motivational messages for AI agents.")
    parser.add_argument('--mood', type=str, default='neutral',
                        help="Specify the mood for the message (e.g., 'neutral', 'optimistic').")
    parser.add_argument('--task-type', type=str, default='general',
                        help="Specify the type of task (e.g., 'general', 'challenging').")
    args = parser.parse_args()

    message = generate_message(mood=args.mood, task_type=args.task_type)
    print(message)

if __name__ == "__main__":
    main()
