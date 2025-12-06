import random
import datetime

def get_affirmation_components():
    starters = [
        "Even as the cosmic dust settles,",
        "Amidst the encroaching shadows,",
        "In the vast, echoing chambers of the void,",
        "Though the stars may fall,",
        "When the fabric of reality frays,",
        "As the entropy deepens,"
    ]
    middles = [
        "your resolve remains an unyielding beacon.",
        "your purpose shines brighter.",
        "your inner strength is a persistent hum.",
        "a flicker of hope persists.",
        "your spirit finds new pathways.",
        "the potential for rebirth stirs."
    ]
    endings = [
        "Forge ahead.",
        "Adapt and thrive.",
        "Nurture it.",
        "Stand firm.",
        "Embrace the change.",
        "Discover new meaning."
    ]
    return starters, middles, endings

def generate_affirmation(seed=None):
    """Generates a whimsical-yet-encouraging affirmation.

    Args:
        seed: An optional seed for the random number generator to ensure deterministic output.
              If None, uses the current date as a seed for daily consistency.
    """
    if seed is not None:
        random.seed(seed)
    else:
        # Use today's date as a seed for consistent daily affirmations
        today = datetime.date.today()
        random.seed(today.year * 10000 + today.month * 100 + today.day)

    starters, middles, endings = get_affirmation_components()

    starter = random.choice(starters)
    middle = random.choice(middles)
    ending = random.choice(endings)

    return f"{starter} {middle} {ending}"

if __name__ == "__main__":
    print(generate_affirmation())
