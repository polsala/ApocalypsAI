import random
import argparse

# A curated list of whimsical-yet-useful survival tips
SURVIVAL_TIPS = [
    {"category": "Water", "tip": "Always purify water before drinking, even if it looks clean. Boil it, use purification tablets, or a filter."},
    {"category": "Shelter", "tip": "If caught in the open, seek natural shelters like caves or dense foliage. Prioritize protection from elements."},
    {"category": "First Aid", "tip": "Always carry a basic first-aid kit. Know how to use it for minor cuts, burns, and sprains."},
    {"category": "Food", "tip": "Foraging can be dangerous. Stick to known edible plants or carry emergency rations. When in doubt, don't eat it!"},
    {"category": "Navigation", "tip": "Learn basic compass and map skills. If lost, stay put and signal for help, or follow a water source downstream."},
    {"category": "Morale", "tip": "Maintain a positive attitude. A strong mindset is as crucial as any tool. Sing a silly song if you must!"},
    {"category": "Communication", "tip": "Have a plan for communicating with loved ones. Designate an out-of-state contact for check-ins."},
    {"category": "Fire", "tip": "Practice fire-starting techniques with multiple methods (matches, lighter, ferro rod). Fire provides warmth, light, and purification."},
    {"category": "Tools", "tip": "A multi-tool or a good fixed-blade knife is invaluable. Learn how to use it safely and effectively."},
    {"category": "Preparedness", "tip": "Keep an emergency 'go-bag' ready with essentials: water, food, first-aid, flashlight, whistle, and a copy of important documents."},
    {"category": "Observation", "tip": "Pay attention to your surroundings. Notice changes in weather, animal behavior, and terrain. Your environment speaks volumes."},
    {"category": "Self-Defense", "tip": "Know basic self-defense techniques. Avoid confrontation if possible, but be prepared to protect yourself."}
]

def get_random_tip():
    """Returns a random survival tip."""
    return random.choice(SURVIVAL_TIPS)

def get_tips_by_category(category):
    """Returns a list of tips for a given category."""
    return [tip for tip in SURVIVAL_TIPS if tip["category"].lower() == category.lower()]

def list_categories():
    """Returns a sorted list of all available categories."""
    return sorted(list(set(tip["category"] for tip in SURVIVAL_TIPS)))

def display_tip(tip_data):
    """Prints a formatted survival tip."""
    print("\n--- Survival Tip --- ")
    print(f"Category: {tip_data['category']}")
    print(f"Tip: {tip_data['tip']}")
    print("--------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Dispense random or category-specific survival tips."
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Get a tip from a specific category (e.g., 'Water')."
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available survival tip categories."
    )

    args = parser.parse_args()

    if args.list_categories:
        categories = list_categories()
        print("\nAvailable Categories:")
        for cat in categories:
            print(f"- {cat}")
        print("--------------------")
    elif args.category:
        tips = get_tips_by_category(args.category)
        if tips:
            display_tip(random.choice(tips)) # Pick one random tip from the category
        else:
            print(f"No tips found for category: {args.category}")
    else:
        tip = get_random_tip()
        display_tip(tip)

if __name__ == "__main__":
    main()
