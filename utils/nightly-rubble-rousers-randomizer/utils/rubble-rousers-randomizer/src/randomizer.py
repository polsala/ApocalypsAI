import random
import argparse

class RubbleRouser:
    def __init__(self):
        self.categories = {
            "item": [
                "A half-eaten can of peaches (still good!)",
                "A rusty multi-tool, missing one blade",
                "A tattered map of the local area, with cryptic annotations",
                "A working flashlight, but no spare batteries",
                "A box of expired but sealed MREs",
                "A child's worn teddy bear",
                "A single, perfectly preserved comic book",
                "A broken radio receiver",
                "A handful of spent bullet casings",
                "A dusty first-aid kit, mostly empty"
            ],
            "encounter": [
                "A lone, wary survivor seeking trade",
                "A pack of feral dogs, eyeing your supplies",
                "Signs of recent raider activity",
                "A small, overgrown garden plot",
                "The distant sound of gunfire",
                "A flock of mutated birds flying overhead",
                "A strange, glowing fungus",
                "A hidden cache, seemingly untouched",
                "A desperate plea for help from a trapped individual",
                "A silent, abandoned drone"
            ],
            "location": [
                "A collapsed overpass, now a makeshift shelter",
                "A flooded subway tunnel, eerily quiet",
                "An abandoned supermarket, picked clean",
                "A fortified gas station, smoke rising from a chimney",
                "A school bus, overturned and used as a barricade",
                "A towering, skeletal skyscraper",
                "A field of strange, mutated flora",
                "A forgotten playground, swings creaking in the wind",
                "A makeshift graveyard marked with crude crosses",
                "A bridge partially destroyed, but still passable on foot"
            ]
        }

    def get_random_find(self, category=None):
        if category and category not in self.categories:
            raise ValueError(f"Invalid category: {category}. Choose from {', '.join(self.categories.keys())}")

        chosen_category_name = category if category else random.choice(list(self.categories.keys()))
        chosen_category_list = self.categories[chosen_category_name]
        chosen_find = random.choice(chosen_category_list)

        return chosen_category_name, chosen_find

def main():
    parser = argparse.ArgumentParser(
        description="Generate random post-apocalyptic finds or encounters."
    )
    parser.add_argument(
        "--category",
        choices=["item", "encounter", "location"],
        help="Specify a category (item, encounter, location). If omitted, a random category will be chosen."
    )

    args = parser.parse_args()

    rouser = RubbleRouser()
    try:
        category_name, find = rouser.get_random_find(args.category)
        print(f"Category: {category_name.replace('_', ' ').title()}")
        print(f"Find: {find}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
