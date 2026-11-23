import sys
import pathlib

# Add the src directory to the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from app import get_possible_recipes

def test_get_possible_recipes_basic():
    available = {"bread", "cheese", "butter"}
    result = get_possible_recipes(available)
    assert "Grilled Cheese" in result
    assert "Cheese Pizza" not in result

def test_no_match():
    available = {"rice", "beans"}
    result = get_possible_recipes(available)
    assert result == []
