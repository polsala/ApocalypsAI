import pytest
from src.app import app, RECIPES, INGREDIENT_NUTRIENTS, DAILY_RECOMMENDED_INTAKES, calculate_total_nutrients, identify_deficiencies

@pytest.fixture
def client():
    """# Mock rationale: Simulates API requests to the Flask app without needing a running server,
    # ensuring deterministic and offline testing of the application logic."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_plan_meal_no_ingredients(client):
    """Test the /plan_meal endpoint with no ingredients provided."""
    response = client.post('/plan_meal', json={'ingredients': []})
    assert response.status_code == 400
    data = response.get_json()
    assert "Please provide a list of available ingredients." in data['message']
    assert data['suggested_recipes'] == []
    assert data['nutrient_nudges'] == {}

def test_plan_meal_basic_ingredients(client):
    """Test the /plan_meal endpoint with ingredients for a simple recipe."""
    ingredients = ["canned beans", "water", "spices", "root vegetables"]
    response = client.post('/plan_meal', json={'ingredients': ingredients})
    assert response.status_code == 200
    data = response.get_json()
    assert "Hearty Bean Stew" in data['suggested_recipes']
    assert data['available_ingredients'] == ingredients
    assert "nutrient_summary_from_pantry" in data
    assert "nutrient_nudges" in data

def test_plan_meal_multiple_recipes(client):
    """Test the /plan_meal endpoint with ingredients for multiple recipes."""
    ingredients = ["canned beans", "water", "spices", "root vegetables", "rice", "dried fruit"]
    response = client.post('/plan_meal', json={'ingredients': ingredients})
    assert response.status_code == 200
    data = response.get_json()
    assert "Hearty Bean Stew" in data['suggested_recipes']
    assert "Rice & Dried Fruit Medley" in data['suggested_recipes']
    assert data['available_ingredients'] == ingredients

def test_plan_meal_nutrient_deficiency(client):
    """Test the /plan_meal endpoint to ensure nutrient deficiencies are reported."""
    ingredients = ["rice", "water"] # Low protein, low vitamins, low fiber
    response = client.post('/plan_meal', json={'ingredients': ingredients})
    assert response.status_code == 200
    data = response.get_json()
    nudges = data['nutrient_nudges']
    assert "protein" in nudges
    assert nudges["protein"] > 0
    assert "vitamins" in nudges
    assert nudges["vitamins"] > 0
    assert "fiber" in nudges
    assert nudges["fiber"] > 0
    assert "iron" in nudges
    assert nudges["iron"] > 0
    assert "fats" in nudges
    assert nudges["fats"] > 0

def test_calculate_total_nutrients():
    """Test the internal calculate_total_nutrients function."""
    ingredients = ["canned beans", "rice", "oil"]
    expected_nutrients = {
        "protein": INGREDIENT_NUTRIENTS["canned beans"]["protein"] + INGREDIENT_NUTRIENTS["rice"]["protein"],
        "fiber": INGREDIENT_NUTRIENTS["canned beans"]["fiber"],
        "iron": INGREDIENT_NUTRIENTS["canned beans"]["iron"],
        "carbs": INGREDIENT_NUTRIENTS["canned beans"]["carbs"] + INGREDIENT_NUTRIENTS["rice"]["carbs"],
        "vitamins": 0, # No vitamins in these specific ingredients in our mock data
        "fats": INGREDIENT_NUTRIENTS["oil"]["fats"]
    }
    # Fill in missing nutrients with 0 for comparison
    for nutrient in DAILY_RECOMMENDED_INTAKES:
        if nutrient not in expected_nutrients:
            expected_nutrients[nutrient] = 0

    result = calculate_total_nutrients(ingredients)
    # Only compare the nutrients we expect to be present or explicitly set to 0
    for nutrient, value in expected_nutrients.items():
        assert result.get(nutrient, 0) == value

def test_identify_deficiencies_no_deficiency():
    """Test identify_deficiencies when all DRIs are met."""
    current = {"protein": 100, "carbs": 300, "fats": 100, "vitamins": 200, "fiber": 50, "iron": 20}
    dris = DAILY_RECOMMENDED_INTAKES
    deficiencies = identify_deficiencies(current, dris)
    assert deficiencies == {}

def test_identify_deficiencies_with_deficiency():
    """Test identify_deficiencies when some DRIs are not met."""
    current = {"protein": 10, "carbs": 100, "fats": 10, "vitamins": 10, "fiber": 5, "iron": 2}
    dris = DAILY_RECOMMENDED_INTAKES
    deficiencies = identify_deficiencies(current, dris)
    assert "protein" in deficiencies
    assert deficiencies["protein"] == 40 # 50 - 10
    assert "carbs" in deficiencies
    assert deficiencies["carbs"] == 100 # 200 - 100
    assert "fats" in deficiencies
    assert deficiencies["fats"] == 50 # 60 - 10
    assert "vitamins" in deficiencies
    assert deficiencies["vitamins"] == 90 # 100 - 10
    assert "fiber" in deficiencies
    assert deficiencies["fiber"] == 25 # 30 - 5
    assert "iron" in deficiencies
    assert deficiencies["iron"] == 8 # 10 - 2
