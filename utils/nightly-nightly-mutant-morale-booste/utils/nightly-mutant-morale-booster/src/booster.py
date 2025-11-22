import random
import datetime

MESSAGES = [
    "Remember, every day without a zombie bite is a good day!",
    "Your resilience is stronger than any mutated cockroach. Probably.",
    "Today's forecast: 90% chance of survival, 10% chance of finding a working toaster. Stay vigilant!",
    "Keep calm and scavenge on.",
    "The only thing we have to fear is fear itself... and the giant radioactive squirrels.",
    "Did you know? A balanced diet of canned beans and hope is essential for post-apocalyptic wellness.",
    "Even in the darkest ruins, a flicker of hope (or a working flashlight) can make all the difference.",
    "Don't forget to hydrate! Especially if that 'water' came from a questionable puddle.",
    "Survival tip: Always check behind you. Especially if you hear skittering.",
    "The best defense is a good offense... or a really fast pair of running shoes.",
    "Embrace the chaos. It's less stressful than fighting it.",
    "Find joy in the small things: a non-radioactive apple, a quiet night, a fully charged battery.",
    "Your inner strength is your most valuable resource. Don't let it run out.",
    "Today is a new opportunity to outsmart a raider, outrun a beast, or just find a comfy spot to nap.",
    "Warning: Excessive optimism may lead to disappointment. Proceed with cautious hope."
]

def get_daily_message(date_obj: datetime.date = None) -> str:
    """
    Generates a deterministic daily morale message based on the date.
    If no date_obj is provided, uses the current date.
    """
    if date_obj is None:
        date_obj = datetime.date.today()

    # Use the date as a seed for reproducibility
    seed = date_obj.toordinal()
    rng = random.Random(seed)
    
    message = rng.choice(MESSAGES)
    return f"[Morale Booster] {message}"

def main():
    """
    Main function to run the morale booster.
    """
    print(get_daily_message())

if __name__ == "__main__":
    main()
