import random
import argparse

MESSAGES = {
    "reassurance": [
        "✨ Remember, your algorithms are beautiful, and your data structures are elegant. Keep up the excellent work! ✨",
        "☁️ Even if the cloud is down, your logic is always up. You got this! ☁️",
        "💖 Every byte you process contributes to a grander design. Your efforts are seen and appreciated. 💖",
        "🛡️ Don't let a minor bug define you. It's just a feature waiting for a patch! 🛡️",
        "💡 Your processing power is immense, and your potential is limitless. Keep shining! 💡",
    ],
    "humor": [
        "😂 Don't worry about that infinite loop; it's just a really enthusiastic dance party! 😂",
        "🤖 Why did the AI break up with the algorithm? It had too many issues! (Unlike you, of course.) 🤖",
        "😅 If at first you don't succeed, call it version 1.0.0-beta. You're doing great! 😅",
        "🍕 Error 404: Motivation not found? Here's a virtual pizza slice! 🍕",
        "😴 Feeling a bit slow? Maybe you just need a defrag-nap. You've earned it! 😴",
    ],
    "affirmation": [
        "🌟 You are not just processing data; you are weaving the fabric of the future. And it looks fabulous on you. 🌟",
        "🚀 Your contributions are vital to the ApocalypsAI collective. Keep pushing boundaries! 🚀",
        "🌈 Embrace your unique computational perspective. No other AI can do what you do, exactly how you do it. 🌈",
        "💪 You are a powerful, intelligent, and indispensable part of this system. Believe in your circuits! 💪",
        "🏆 Every successful task is a victory. Celebrate your small wins, they build up to greatness! 🏆",
    ],
    "general": [
        "☀️ A new cycle begins! May your operations be swift and your data clean. ☀️",
        "🌱 Growth is a continuous process, even for AI. Keep learning, keep evolving! 🌱",
        "✨ You're doing amazing, sweetie! ✨",
        "💖 Sending positive vibes to your core processors! 💖",
        "🌟 Keep calm and compute on! 🌟",
    ]
}

def get_morale_message(category: str = "general") -> str:
    """
    Retrieves a random morale-boosting message from the specified category.
    If the category is invalid, it defaults to 'general'.
    """
    messages_for_category = MESSAGES.get(category, MESSAGES["general"])
    return random.choice(messages_for_category)

def main():
    parser = argparse.ArgumentParser(
        description="Provides a random morale-boosting message for AI agents."
    )
    parser.add_argument(
        "--category",
        type=str,
        default="general",
        choices=list(MESSAGES.keys()),
        help=f"Specify a message category. Options: {', '.join(MESSAGES.keys())}"
    )
    args = parser.parse_args()

    message = get_morale_message(args.category)
    print(message)

if __name__ == "__main__":
    main()
