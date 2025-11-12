import random

SURVIVAL_SKILLS = [
    "Learn to identify 3 edible wild plants in your local area (and 1 poisonous one!).",
    "Practice tying 5 essential knots: bowline, clove hitch, square knot, sheet bend, taut-line hitch.",
    "Build a small, temporary shelter using only natural materials found nearby.",
    "Figure out how to purify 1 liter of water using only household items.",
    "Map your immediate neighborhood, identifying potential water sources, shelter, and escape routes.",
    "Practice starting a fire without matches or a lighter (e.g., ferro rod, friction fire).",
    "Learn basic first aid for cuts, burns, and sprains.",
    "Devise a communication plan with a loved one in case of power/internet outage.",
    "Spend an hour observing your surroundings in silence, noting wildlife and potential resources.",
    "Repurpose an old item (e.g., a plastic bottle, old clothes) into something useful."
]

def get_random_skill():
    """Returns a random survival skill challenge."""
    return random.choice(SURVIVAL_SKILLS)

def main():
    """Main function to run the scrambler and print a challenge."""
    challenge = get_random_skill()
    print(f"Your survival challenge for today: {challenge}")

if __name__ == "__main__":
    main()
