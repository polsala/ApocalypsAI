import argparse
import json

SKILLS_DATA = {
    "water_purification": {
        "title": "Water Purification",
        "description": "Ensuring safe drinking water is paramount for survival.",
        "steps": [
            "1. Filter large debris using cloth.",
            "2. Boil water vigorously for at least 1 minute (3 minutes at high altitudes).",
            "3. Alternatively, use chemical tablets or a portable filter.",
            "4. Let cool before drinking."
        ],
        "keywords": ["water", "purify", "drink", "hydration"]
    },
    "basic_first_aid": {
        "title": "Basic First Aid",
        "description": "Treating minor injuries can prevent serious complications.",
        "steps": [
            "1. Assess the situation for immediate dangers.",
            "2. Stop bleeding: Apply direct pressure to wounds.",
            "3. Clean wounds: Use clean water and soap if available.",
            "4. Cover wounds: Use sterile dressing or clean cloth.",
            "5. Treat burns: Cool with water, cover loosely.",
            "6. Immobilize fractures: Splint if necessary."
        ],
        "keywords": ["first aid", "injury", "wound", "burn", "fracture"]
    },
    "fire_starting": {
        "title": "Fire Starting",
        "description": "Fire provides warmth, cooks food, purifies water, and offers psychological comfort.",
        "steps": [
            "1. Gather tinder (fine, dry material), kindling (small twigs), and fuel (larger wood).",
            "2. Build a small teepee or log cabin structure.",
            "3. Use a spark (ferro rod, lighter, matches) to ignite tinder.",
            "4. Gently blow on the flame to encourage growth.",
            "5. Gradually add kindling, then fuel."
        ],
        "keywords": ["fire", "warmth", "cook", "signal"]
    }
}

def list_skills():
    """Lists all available survival skills."""
    print("Available Survival Skills:")
    for key, data in SKILLS_DATA.items():
        print(f"- {data['title']} ({key})")

def get_skill_details(skill_key):
    """Retrieves and prints details for a specific skill."""
    skill = SKILLS_DATA.get(skill_key)
    if skill:
        print(f"\n--- {skill['title']} ---")
        print(f"Description: {skill['description']}")
        print("\nSteps:")
        for step in skill['steps']:
            print(f"  {step}")
        print(f"\nKeywords: {', '.join(skill['keywords'])}")
    else:
        print(f"Error: Skill '{skill_key}' not found. Use 'list' to see available skills.")
        return 1
    return 0

def search_skills(query):
    """Searches for skills by title, description, or keywords."""
    query = query.lower()
    found_skills = []
    for key, data in SKILLS_DATA.items():
        if query in data['title'].lower() or \
           query in data['description'].lower() or \
           any(query in k.lower() for k in data['keywords']):
            found_skills.append(data['title'])
    
    if found_skills:
        print(f"Skills matching '{query}':")
        for skill_title in found_skills:
            print(f"- {skill_title}")
    else:
        print(f"No skills found matching '{query}'.")
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Survival Skill Scribe: Your quick reference for essential survival knowledge."
    )
    parser.add_argument(
        "action",
        choices=["list", "get", "search"],
        help="Action to perform: 'list' all skills, 'get' details for a specific skill, or 'search' for skills by keyword."
    )
    parser.add_argument(
        "skill_key_or_query",
        nargs="?",
        help="Skill key for 'get' action (e.g., 'water_purification') or search query for 'search' action."
    )

    args = parser.parse_args()

    if args.action == "list":
        list_skills()
    elif args.action == "get":
        if not args.skill_key_or_query:
            parser.error("The 'get' action requires a skill key.")
        exit_code = get_skill_details(args.skill_key_or_query)
        exit(exit_code)
    elif args.action == "search":
        if not args.skill_key_or_query:
            parser.error("The 'search' action requires a search query.")
        exit_code = search_skills(args.skill_key_or_query)
        exit(exit_code)

if __name__ == "__main__":
    main()
