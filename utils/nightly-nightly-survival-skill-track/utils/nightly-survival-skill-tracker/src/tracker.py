import argparse
import json
import os

SKILLS_FILE = os.path.join(os.path.dirname(__file__), 'skills.json')

def load_skills():
    """Loads skills from the JSON file."""
    if not os.path.exists(SKILLS_FILE):
        return {}
    with open(SKILLS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {} # Return empty if file is corrupt

def save_skills(skills):
    """Saves skills to the JSON file."""
    with open(SKILLS_FILE, 'w') as f:
        json.dump(skills, f, indent=4)

def add_skill(skill_name):
    """Adds a new skill with a default rating of 1."""
    skills = load_skills()
    if skill_name in skills:
        print(f"Skill '{skill_name}' already exists.")
    else:
        skills[skill_name] = 1
        save_skills(skills)
        print(f"Skill '{skill_name}' added with rating 1.")

def rate_skill(skill_name, rating):
    """Rates an existing skill (1-5)."""
    skills = load_skills()
    if skill_name not in skills:
        print(f"Skill '{skill_name}' not found. Add it first.")
        return
    if not 1 <= rating <= 5:
        print("Rating must be between 1 and 5.")
        return
    skills[skill_name] = rating
    save_skills(skills)
    print(f"Skill '{skill_name}' rated {rating}.")

def list_skills():
    """Lists all tracked skills and their ratings."""
    skills = load_skills()
    if not skills:
        print("No skills tracked yet. Add some!")
        return
    print("\n--- Your Survival Skills ---")
    for skill, rating in sorted(skills.items()):
        print(f"- {skill}: {rating}/5")
    print("--------------------------")

def suggest_improvement():
    """Suggests the lowest-rated skill for improvement, picking alphabetically if tied."""
    skills = load_skills()
    if not skills:
        print("No skills to suggest. Add some first!")
        return
    
    lowest_rated_skill = None
    min_rating = 6 # Higher than max possible rating

    for skill, rating in skills.items():
        if rating < min_rating:
            min_rating = rating
            lowest_rated_skill = skill
        elif rating == min_rating and lowest_rated_skill is not None:
            # If multiple skills have the same lowest rating, pick alphabetically
            if skill < lowest_rated_skill:
                lowest_rated_skill = skill

    if lowest_rated_skill:
        print(f"\nSuggestion: Focus on improving '{lowest_rated_skill}' (current rating: {min_rating}/5).")
    else:
        print("Could not find a skill to suggest for improvement.")

def main():
    parser = argparse.ArgumentParser(
        description="Track and rate your apocalypse survival skills."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add skill command
    add_parser = subparsers.add_parser('add', help='Add a new survival skill.')
    add_parser.add_argument('skill_name', type=str, help='The name of the skill to add.')

    # Rate skill command
    rate_parser = subparsers.add_parser('rate', help='Rate an existing survival skill.')
    rate_parser.add_argument('skill_name', type=str, help='The name of the skill to rate.')
    rate_parser.add_argument('rating', type=int, help='Your proficiency rating (1-5).')

    # List skills command
    list_parser = subparsers.add_parser('list', help='List all tracked skills.')

    # Suggest improvement command
    suggest_parser = subparsers.add_parser('suggest', help='Get a suggestion for skill improvement.')

    args = parser.parse_args()

    if args.command == 'add':
        add_skill(args.skill_name)
    elif args.command == 'rate':
        rate_skill(args.skill_name, args.rating)
    elif args.command == 'list':
        list_skills()
    elif args.command == 'suggest':
        suggest_improvement()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
