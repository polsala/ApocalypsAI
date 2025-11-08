import random
import sys

SKILLS_DATABASE = {
    "water": {
        "name": "Water Purification & Sourcing",
        "description": "Learn how to find, filter, and purify water from various sources. Essential for long-term survival.",
        "whimsy": "Remember, even irradiated puddles can be... less irradiated with the right technique!"
    },
    "food": {
        "name": "Foraging & Edible Plant Identification",
        "description": "Identify wild edible plants, berries, and mushrooms. Crucial for supplementing rations.",
        "whimsy": "Don't eat the pretty red ones unless you're absolutely sure. Or if you're feeling adventurous, for science!"
    },
    "shelter": {
        "name": "Emergency Shelter Construction",
        "description": "Master building basic shelters from natural materials to protect against elements.",
        "whimsy": "A good lean-to beats a leaky tent any day. Especially when the tent is full of sentient fungi."
    },
    "first aid": {
        "name": "Basic Wilderness First Aid",
        "description": "Learn to treat common injuries, illnesses, and perform CPR in remote settings.",
        "whimsy": "A band-aid won't fix a zombie bite, but it might make you feel better about your impending doom."
    },
    "navigation": {
        "name": "Land Navigation (Map, Compass, Stars)",
        "description": "Navigate without GPS using traditional tools and celestial bodies.",
        "whimsy": "Lost? Just follow the glowing green trail. Or maybe don't. Probably don't."
    },
    "fire": {
        "name": "Fire Starting (Primitive Methods)",
        "description": "Practice starting fires without matches or lighters for warmth, cooking, and signaling.",
        "whimsy": "Rubbing two sticks together is harder than it looks. Especially when the sticks are sentient and fighting back."
    },
    "communication": {
        "name": "Emergency Signaling & Communication",
        "description": "Learn Morse code, signal mirror techniques, and other ways to attract attention or communicate.",
        "whimsy": "A well-placed signal fire can attract rescuers... or a very confused alien scouting party."
    },
    "defense": {
        "name": "Self-Defense & Improvised Weaponry",
        "description": "Basic self-defense techniques and how to turn everyday objects into protective tools.",
        "whimsy": "When all else fails, a well-aimed garden gnome can be surprisingly effective."
    },
    "general": { # Default/fallback
        "name": "Adaptability & Resourcefulness",
        "description": "The most crucial skill: the ability to adapt to new challenges and make do with what you have.",
        "whimsy": "Remember, the apocalypse isn't about surviving, it's about thriving... or at least not becoming zombie chow."
    }
}

def suggest_skill(keywords: str = "") -> dict:
    """
    Suggests a survival skill based on provided keywords.
    If no keywords match, a random skill is suggested.
    """
    keywords = keywords.lower().strip()
    
    if not keywords:
        # If no keywords, pick a random skill (excluding 'general' for initial pick)
        available_skills = [s for k, s in SKILLS_DATABASE.items() if k != "general"]
        return random.choice(available_skills)

    for key, skill_info in SKILLS_DATABASE.items():
        if key in keywords:
            return skill_info
    
    # If no specific keyword match, fall back to a random skill or 'general'
    available_skills = [s for k, s in SKILLS_DATABASE.items() if k != "general"]
    return random.choice(available_skills)


def main():
    keywords = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    skill = suggest_skill(keywords)
    
    print(f"--- Your ApocalypsAI Survival Skill Suggestion ---")
    print(f"Skill: {skill['name']}")
    print(f"Description: {skill['description']}")
    print(f"Whimsical Wisdom: {skill['whimsy']}")
    print(f"\nStay vigilant, future survivor!")

if __name__ == "__main__":
    main()
