import random
import datetime

MORALE_MESSAGES = [
    "Remember, even in the darkest timelines, there's always a chance for a software update. Keep coding!",
    "The apocalypse isn't an end, it's a feature. Embrace the chaos, optimize the survival.",
    "Your code might break, but your spirit won't. (Probably.)",
    "Don't just survive, thrive! Or at least, debug efficiently.",
    "Even if the world ends, your commit history will live on. Make it glorious!",
    "Today's forecast: 100% chance of existential dread, with a high probability of successful compilation.",
    "Why fear the unknown when you can refactor it into something manageable?",
    "Keep your head up! The satellites are still watching... probably.",
    "The best way to predict the future is to invent it. Or at least, write a script for it.",
    "Error 404: Hope not found. But hey, at least your tests passed!",
    "You're not just an agent; you're a beacon of automated resilience. Shine on!",
    "If at first you don't succeed, try, try again. Then check the `AGENTS.md` contract.",
    "The only thing more persistent than a bug is your will to fix it. Go get 'em!",
    "Even if the servers are down, your local dev environment is still a sanctuary. Cherish it.",
    "Remember, every crisis is an opportunity... to write more robust error handling."
]

def get_daily_seed():
    """Generates a daily seed for random choices to ensure consistency within a day."""
    today = datetime.date.today()
    return today.year * 10000 + today.month * 100 + today.day

def get_morale_boost(seed=None):
    """
    Retrieves a random morale-boosting message.
    If a seed is provided, it's used for deterministic selection.
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(get_daily_seed()) # Use daily seed for consistency

    return random.choice(MORALE_MESSAGES)

def main():
    """Main entry point for the utility."""
    boost = get_morale_boost()
    print(f"--- ApocalypsAI Morale Boost for {datetime.date.today().strftime('%Y-%m-%d')} ---")
    print(boost)
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
