from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock rationale: Hardcoded recipes and nutrient data are used to ensure deterministic test results
# without external dependencies or complex database setups.
RECIPES = [
    {
        "name": "Hearty Bean Stew",
        "ingredients": ["canned beans", "water", "spices", "root vegetables"],
        "nutrients_per_serving": {"protein": 20, "fiber": 15, "iron": 5, "carbs": 30, "vitamins": 10}
    },
    {
        "name": "Rice & Dried Fruit Medley",
        "ingredients": ["rice", "dried fruit", "water"],
        "nutrients_per_serving": {"carbs": 50, "vitamins": 20, "fiber": 5}
    },
    {
        "name": "Foraged Greens Salad",
        "ingredients": ["foraged greens", "oil", "vinegar"],
        "nutrients_per_serving": {"vitamins": 30, "fiber": 10, "fats": 10}
    },
    {
        "name": "Basic Protein Bar (DIY)",
        "ingredients": ["protein powder", "nut butter", "honey"],
        "nutrients_per_serving": {"protein": 30, "fats": 20, "carbs": 20}
    }
]

# Mock rationale: Hardcoded nutrient data for individual ingredients for deterministic testing.
INGREDIENT_NUTRIENTS = {
    "canned beans": {"protein": 10, "fiber": 8, "iron": 3, "carbs": 15},
    "rice": {"carbs": 25, "protein": 2},
    "dried fruit": {"carbs": 25, "vitamins": 10, "fiber": 2},
    "foraged greens": {"vitamins": 15, "fiber": 5},
    "oil": {"fats": 10},
    "vinegar": {},
    "water": {},
    "spices": {},
    "root vegetables": {"carbs": 15, "vitamins": 5, "fiber": 5},
    "protein powder": {"protein": 25},
    "nut butter": {"fats": 15, "protein": 5},
    "honey": {"carbs": 15}
}

# Mock rationale: Simplified DRIs for deterministic nutrient deficiency calculations.
DAILY_RECOMMENDED_INTAKES = {
    "protein": 50,
    "carbs": 200,
    "fats": 60,
    "vitamins": 100,
    "fiber": 30,
    "iron": 10
}

def calculate_total_nutrients(ingredients):
    """Calculates total nutrients from a list of available ingredients."""
    total_nutrients = {nutrient: 0 for nutrient in DAILY_RECOMMENDED_INTAKES}
    for ingredient in ingredients:
        if ingredient in INGREDIENT_NUTRIENTS:
            for nutrient, amount in INGREDIENT_NUTRIENTS[ingredient].items():
                total_nutrients[nutrient] += amount
    return total_nutrients

def identify_deficiencies(current_nutrients, dris):
    """Compares current nutrients to DRIs and identifies deficiencies."""
    deficiencies = {}
    for nutrient, required in dris.items():
        if current_nutrients.get(nutrient, 0) < required:
            deficiencies[nutrient] = required - current_nutrients.get(nutrient, 0)
    return deficiencies

@app.route('/plan_meal', methods=['POST'])
def plan_meal():
    data = request.get_json()
    available_ingredients = data.get('ingredients', [])

    if not available_ingredients:
        return jsonify({"message": "Please provide a list of available ingredients.", "suggestions": [], "nutrient_summary": {}, "deficiencies": {}}), 400

    possible_recipes = []
    for recipe in RECIPES:
        if all(ing in available_ingredients for ing in recipe["ingredients"]):
            possible_recipes.append(recipe["name"])

    current_nutrients = calculate_total_nutrients(available_ingredients)
    deficiencies = identify_deficiencies(current_nutrients, DAILY_RECOMMENDED_INTAKES)

    response = {
        "message": "Nutrient Noodler's Daily Digest:",
        "available_ingredients": available_ingredients,
        "suggested_recipes": possible_recipes,
        "nutrient_summary_from_pantry": current_nutrients,
        "nutrient_nudges": deficiencies
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
