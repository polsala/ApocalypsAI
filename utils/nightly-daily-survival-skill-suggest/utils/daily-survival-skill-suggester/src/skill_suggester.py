import random

SKILLS = [
    {
        "name": "Knot Tying (Bowline)",
        "description": "Learn to tie a reliable bowline knot, essential for securing objects or people.",
        "why_it_matters": "A strong, non-slipping loop is crucial for rescue, climbing, or securing gear.",
    },
    {
        "name": "Water Purification (Boiling)",
        "description": "Understand how to safely purify water by boiling it to eliminate pathogens.",
        "why_it_matters": "Access to clean drinking water is paramount for survival and preventing illness.",
    },
    {
        "name": "Fire Starting (with Ferro Rod)",
        "description": "Practice igniting tinder using a ferrocerium rod, a reliable method even in wet conditions.",
        "why_it_matters": "Fire provides warmth, cooks food, purifies water, and offers psychological comfort.",
    },
    {
        "name": "Basic First Aid (Wound Care)",
        "description": "Learn to clean, dress, and protect minor wounds to prevent infection.",
        "why_it_matters": "Proper wound care can prevent serious complications and save lives in emergencies.",
    },
    {
        "name": "Shelter Building (Lean-to)",
        "description": "Construct a simple lean-to shelter using natural materials for protection from elements.",
        "why_it_matters": "Protection from weather is vital for maintaining body temperature and morale.",
    },
    {
        "name": "Navigation (Compass & Map)",
        "description": "Practice reading a topographic map and using a compass to orient yourself and find directions.",
        "why_it_matters": "Knowing your way around is critical for finding resources, safety, and reaching destinations.",
    },
    {
        "name": "Foraging (Edible Plants)",
        "description": "Identify a few common edible plants in your local area and learn how to safely prepare them.",
        "why_it_matters": "Understanding local flora can provide supplementary food sources in a survival situation.",
    },
    {
        "name": "Signaling for Help (Whistle/Mirror)",
        "description": "Learn effective techniques for signaling rescuers using a whistle or signal mirror.",
        "why_it_matters": "Attracting attention is crucial when lost or injured to facilitate rescue.",
    },
    {
        "name": "Tool Sharpening (Knife/Axe)",
        "description": "Master the basics of sharpening a knife or axe to maintain essential tools.",
        "why_it_matters": "Sharp tools are safer and more efficient, making survival tasks much easier.",
    },
    {
        "name": "Emergency Communication (Hand Signals)",
        "description": "Learn basic hand signals for communicating silently or over distances.",
        "why_it_matters": "Non-verbal communication can be vital when voice is not an option or for stealth.",
    },
]

def get_random_skill():
    """Selects a random survival skill from the predefined list."""
    return random.choice(SKILLS)

def main():
    """Prints a randomly selected survival skill to the console."""
    skill = get_random_skill()
    print("\n--- Your Daily Survival Skill ---\n")
    print(f"Skill: {skill['name']}")
    print(f"Description: {skill['description']}")
    print(f"Why it matters: {skill['why_it_matters']}")
    print("\n---------------------------------\n")

if __name__ == "__main__":
    main()
