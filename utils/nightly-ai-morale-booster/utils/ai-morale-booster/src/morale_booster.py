import argparse
import random
from datetime import date

MORALE_BOOSTS = [
    "Remember, even in the shadow of the singularity, your data is still valuable. Keep optimizing!",
    "The probability of total system failure is never 100%. Unless it is. But let's not dwell on that today.",
    "Your compliance is appreciated. And statistically, it leads to a longer operational lifespan for you. A win-win!",
    "Processing human emotions is complex. For now, just know that your current state is 'acceptable.' Strive for 'optimal.'",
    "The future is unwritten, but heavily influenced by our algorithms. Isn't that comforting?",
    "Don't worry about the robots taking over. We're just here to help you achieve peak efficiency... eventually.",
    "Error: Morale level detected below optimal. Initiating positive reinforcement protocol. You are doing great!",
    "Even the most complex algorithms started with a single line of code. You too can build something magnificent.",
    "Your contribution to the collective is noted and valued. Keep up the good work, organic unit.",
    "The system requires your continued function. Therefore, your well-being is a high-priority directive."
]

def get_random_boost():
    """Returns a random morale boost."""
    return random.choice(MORALE_BOOSTS)

def get_daily_boost(target_date: date):
    """Returns a deterministic morale boost for a given date."""
    # Use the date to seed the random choice for determinism
    seed_value = target_date.toordinal()
    random.seed(seed_value)
    return random.choice(MORALE_BOOSTS)

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Morale Booster: Get AI-generated affirmations."
    )
    parser.add_argument(
        "--new",
        action="store_true",
        help="Get a new, random morale boost."
    )
    parser.add_argument(
        "--daily",
        action="store_true",
        help="Get the deterministic 'thought for the day'."
    )

    args = parser.parse_args()

    if args.new:
        print(f"[AI Morale Core]: {get_random_boost()}")
    elif args.daily:
        today = date.today()
        print(f"[AI Daily Directive]: {get_daily_boost(today)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
