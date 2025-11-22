import random

MORALE_MESSAGES = [
    "Remember: Even a broken clock is right twice a day. Just like your Geiger counter.",
    "Survival Tip: Always check for extra limbs before sharing your last can of beans.",
    "Keep your spirits high! The raiders might be less likely to notice you if you're humming a jaunty tune.",
    "Today's wisdom: A well-maintained rusty spork is worth two shiny, broken ones.",
    "Don't let the glowing puddles get you down. They're just... extra sparkly!",
    "Even in the darkest wasteland, there's always a chance to find a slightly less broken radio.",
    "Thought for the day: Your biggest asset isn't your weapon, it's your ability to improvise with a rubber chicken.",
    "Survival is not just about staying alive, it's about finding joy in the small things, like uncontaminated water.",
    "A true survivor knows that duct tape can fix anything, including a shattered dream (temporarily).",
    "When life gives you irradiated lemons, make... well, don't make lemonade. Just avoid them."
]

def get_random_morale_message():
    """
    Selects a random morale-boosting message from the predefined list.
    """
    return random.choice(MORALE_MESSAGES)

def main():
    """
    Main function to run the morale booster.
    """
    message = get_random_morale_message()
    print(f"[MUTANT MORALE BOOSTER] {message}")

if __name__ == "__main__":
    main()
