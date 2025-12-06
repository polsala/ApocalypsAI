import random

SKILLS = [
    "Practice knot-tying (bowline, square knot, sheet bend).",
    "Identify 3 edible wild plants in your area (with caution and expert guidance!).",
    "Learn basic first aid for cuts, burns, and sprains.",
    "Check your emergency water supply and rotate if needed.",
    "Practice starting a fire without matches (e.g., ferro rod, magnifying glass).",
    "Review your emergency communication plan with your household.",
    "Sharpen your most-used utility knife or multi-tool.",
    "Learn to purify water using common household items (e.g., bleach, boiling).",
    "Practice basic self-defense moves or situational awareness exercises.",
    "Organize your bug-out bag/go-bag and check expiry dates on food/meds.",
    "Map out alternative escape routes from your home/workplace.",
    "Learn how to safely turn off utilities (water, gas, electricity) in your home.",
    "Practice basic navigation using a compass and a physical map.",
    "Assemble a small, portable repair kit for minor fixes.",
    "Learn to identify common weather patterns and interpret forecasts."
]

def get_random_skill():
    """Selects a random survival skill from the predefined list."""
    return random.choice(SKILLS)

def run_scrambler():
    """Executes the main logic of the scrambler, printing a random skill."""
    skill = get_random_skill()
    print(f"Your survival task for today: {skill}")

if __name__ == "__main__":
    run_scrambler()
