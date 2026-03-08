import pathlib
import tempfile
import csv
import sys

# Import the module under test
from src import app as pantry_app

def write_inventory(tmp_path, items):
    """Helper to write a CSV inventory file given an iterable of ingredient strings."""
    inventory_file = tmp_path / "inventory.csv"
    with inventory_file.open("w", newline="") as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow([item])
    return inventory_file

def test_suggest_bean_soup(tmp_path, monkeypatch):
    # Mock the expected location of the inventory file inside the container
    inventory_file = write_inventory(tmp_path, ["beans", "water", "salt"])
    monkeypatch.setattr(pathlib.Path, "is_file", lambda self: True if self == pathlib.Path("/data/inventory.csv") else pathlib.Path.is_file(self))
    monkeypatch.setattr(pathlib.Path, "open", lambda self, *args, **kwargs: inventory_file.open(*args, **kwargs) if self == pathlib.Path("/data/inventory.csv") else pathlib.Path.open(self, *args, **kwargs))
    inventory = pantry_app.load_inventory(pathlib.Path("/data/inventory.csv"))
    suggestions = pantry_app.suggest_recipes(inventory)
    assert "Bean Soup" in suggestions
    assert len(suggestions) == 1

def test_no_matching_recipes(tmp_path, monkeypatch):
    inventory_file = write_inventory(tmp_path, ["flour", "sugar"])
    monkeypatch.setattr(pathlib.Path, "is_file", lambda self: True if self == pathlib.Path("/data/inventory.csv") else pathlib.Path.is_file(self))
    monkeypatch.setattr(pathlib.Path, "open", lambda self, *args, **kwargs: inventory_file.open(*args, **kwargs) if self == pathlib.Path("/data/inventory.csv") else pathlib.Path.open(self, *args, **kwargs))
    inventory = pantry_app.load_inventory(pathlib.Path("/data/inventory.csv"))
    suggestions = pantry_app.suggest_recipes(inventory)
    assert suggestions == []

# Mock rationale: The tests replace filesystem checks to point to a temporary CSV file, ensuring they run offline and deterministically.
