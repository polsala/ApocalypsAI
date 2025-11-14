import sys
import argparse

SKILLS_DATABASE = {
    "water": {
        "skill": "Water Purification",
        "description": "Learn to filter and boil water from natural sources. A life-saver when the taps run dry. Don't forget a portable filter!",
        "keywords": ["hydration", "drink", "thirst"]
    },
    "food": {
        "skill": "Foraging & Edible Plant Identification",
        "description": "Distinguish between nourishing greens and deadly berries. Your stomach will thank you, if you don't poison yourself first.",
        "keywords": ["hunger", "eat", "sustenance"]
    },
    "shelter": {
        "skill": "Improvised Shelter Construction",
        "description": "Master the art of building temporary shelters from natural materials. A cozy den beats a cold night under the stars (or radioactive fallout).",
        "keywords": ["home", "protection", "roof"]
    },
    "first aid": {
        "skill": "Basic Wilderness First Aid",
        "description": "Treat cuts, sprains, and minor injuries with limited supplies. A bandage and some antiseptic can prevent a minor scrape from becoming a major problem.",
        "keywords": ["medical", "injury", "health"]
    },
    "defense": {
        "skill": "Self-Defense & Situational Awareness",
        "description": "Develop basic self-defense techniques and learn to assess threats. Knowing when to fight, flee, or hide is crucial for survival.",
        "keywords": ["security", "protection", "threat"]
    },
    "navigation": {
        "skill": "Map Reading & Compass Use",
        "description": "Navigate without GPS. The old ways are often the best ways when satellites are space junk. Don't get lost in the wasteland!",
        "keywords": ["direction", "path", "travel"]
    },
    "fire": {
        "skill": "Fire Starting (Primitive Methods)",
        "description": "Learn to make fire without matches or lighters. Essential for warmth, cooking, and signaling. Rub two sticks together like your ancestors!",
        "keywords": ["heat", "cook", "light"]
    }
}

def get_skill_suggestion(keyword: str) -> dict | None:
    """
    Suggests a survival skill based on a keyword.
    Performs a case-insensitive search across main keywords and secondary keywords.
    """
    keyword_lower = keyword.lower()
    for category, data in SKILLS_DATABASE.items():
        if keyword_lower == category.lower() or keyword_lower in [k.lower() for k in data.get("keywords", [])]:
            return data
    return None

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Survival Skill Suggester: Get a whimsical-yet-useful survival skill suggestion."
    )
    parser.add_argument(
        "keyword",
        type=str,
        help="A keyword related to survival (e.g., 'water', 'food', 'shelter', 'defense')."
    )
    args = parser.parse_args()

    suggestion = get_skill_suggestion(args.keyword)

    if suggestion:
        print(f"Skill: {suggestion['skill']}")
        print(f"Description: {suggestion['description']}")
    else:
        print(f"No specific skill found for '{args.keyword}'. Try 'water', 'food', 'shelter', 'first aid', 'defense', 'navigation', or 'fire'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
