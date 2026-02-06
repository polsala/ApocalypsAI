import sys
import random

def generate_recipe(ingredients_str):
    ingredients = [i.strip() for i in ingredients_str.split(',') if i.strip()]

    adjectives = [
        "Rusty", "Glow-in-the-Dark", "Forgotten", "Dusty", "Quantum",
        "Temporal", "Whispering", "Silent", "Crunchy", "Slimey",
        "Irradiated", "Salvaged", "Makeshift", "Desolate", "Wasteland"
    ]
    nouns = [
        "Stew", "Ration", "Pudding", "Surprise", "Concoction",
        "Mash", "Delight", "Elixir", "Nuggets", "Crumble",
        "Forage", "Broth", "Goulash", "Jelly", "Pâté"
    ]
    verbs = [
        "Scramble", "Boil", "Fry", "Bake", "Reconstitute",
        "Ferment", "Distill", "Combine", "Macerate", "Pulverize",
        "Render", "Simmer", "Char", "Infuse", "Dehydrate"
    ]
    methods = [
        "over a flickering barrel fire",
        "using a solar-powered dehydrator",
        "with salvaged kitchenware",
        "in a makeshift pressure cooker",
        "under the watchful eye of the moon",
        "in a repurposed oil drum",
        "with a jury-rigged solar oven",
        "by the light of a dying sun"
    ]

    if not ingredients:
        ingredients = ["mystery ingredient"]
        recipe_name_ingredient = "Mystery"
    else:
        recipe_name_ingredient = random.choice(ingredients).title()

    random_adj = random.choice(adjectives)
    random_noun = random.choice(nouns)
    random_verb = random.choice(verbs)
    random_method = random.choice(methods)

    recipe_name = f"--- The {random_adj} {recipe_name_ingredient} {random_noun} ---"
    description = f"A hearty {random_noun.lower()} to {random_verb.lower()} your spirits, featuring the rare {random.choice(ingredients)}."
    instructions = (
        f"Instructions:\n"
        f"1. Gather your {', '.join(ingredients)}.\n"
        f"2. {random_verb.capitalize()} them {random_method}.\n"
        f"3. Serve with a side of existential dread."
    )

    return f"{recipe_name}\n{description}\n\n{instructions}"

if __name__ == "__main__":
    input_ingredients = sys.argv[1] if len(sys.argv) > 1 else ""
    print(generate_recipe(input_ingredients))
