import pytest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime

# Mock rationale: We need to ensure tests are deterministic and don't rely on actual file system operations
# or the current date/time, which would make tests non-repeatable.
# `mock_open` simulates file I/O, and `patch('os.path.exists')` controls file existence checks.
# `patch('datetime')` allows us to fix the 'added_date' for consistent item creation.

# Import the class to be tested
from src.manifest_manager import ManifestManager

@pytest.fixture
def temp_manifest_file(tmp_path):
    """Fixture to provide a temporary manifest file path."""
    return tmp_path / "test_manifest.json"

@pytest.fixture
def manager(temp_manifest_file):
    """Fixture to provide a ManifestManager instance with a temporary file."""
    with patch('datetime.now') as mock_now:
        mock_now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Fixed date for deterministic tests
        yield ManifestManager(manifest_file=str(temp_manifest_file))
    # Clean up after test if needed, though tmp_path handles most of it.

def test_initialization_empty_file(temp_manifest_file):
    """Test that manager initializes with an empty manifest if file doesn't exist."""
    assert not temp_manifest_file.exists()
    manager = ManifestManager(manifest_file=str(temp_manifest_file))
    assert manager.items == []
    assert manager._next_id == 1

def test_initialization_existing_file(temp_manifest_file):
    """Test that manager loads items from an existing manifest file."""
    initial_data = [
        {"id": 1, "name": "Water Bottle", "description": "Empty", "quantity": 1, "tags": ["hydration"], "added_date": "2023-10-26T10:00:00"},
        {"id": 2, "name": "Canned Beans", "description": "Kidney beans", "quantity": 3, "tags": ["food"], "added_date": "2023-10-26T11:00:00"}
    ]
    temp_manifest_file.write_text(json.dumps(initial_data))

    manager = ManifestManager(manifest_file=str(temp_manifest_file))
    assert len(manager.items) == 2
    assert manager.items[0]['name'] == "Water Bottle"
    assert manager._next_id == 3 # Should pick up from max ID + 1

def test_initialization_corrupted_file(temp_manifest_file, capsys):
    """Test that manager handles corrupted JSON files gracefully."""
    temp_manifest_file.write_text("this is not valid json {")
    manager = ManifestManager(manifest_file=str(temp_manifest_file))
    assert manager.items == []
    assert manager._next_id == 1
    captured = capsys.readouterr()
    assert "Warning: Manifest file" in captured.out
    assert "is corrupted" in captured.out

def test_add_item(manager):
    """Test adding a single item."""
    item = manager.add_item("Flashlight", "Needs batteries", 1, "tool, light")
    assert len(manager.items) == 1
    assert item['name'] == "Flashlight"
    assert item['quantity'] == 1
    assert "tool" in item['tags']
    assert item['id'] == 1
    assert item['added_date'] == "2023-10-27T10:00:00"

    item2 = manager.add_item("Rope", "50ft nylon", 1, "utility")
    assert len(manager.items) == 2
    assert item2['id'] == 2

def test_list_items(manager):
    """Test listing items, ensuring they are sorted by ID."""
    manager.add_item("Axe", "Sharp", 1, "tool")
    manager.add_item("Bandages", "First aid", 5, "medical")
    manager.add_item("Water Purifier", "Portable", 1, "hydration, tool")

    items = manager.list_items()
    assert len(items) == 3
    assert items[0]['name'] == "Axe"
    assert items[1]['name'] == "Bandages"
    assert items[2]['name'] == "Water Purifier"
    assert items[0]['id'] == 1
    assert items[1]['id'] == 2
    assert items[2]['id'] == 3

def test_search_items_by_name(manager):
    """Test searching items by name."""
    manager.add_item("Canned Peaches", "Sweet", 2, "food")
    manager.add_item("Canned Tuna", "Protein", 4, "food")
    manager.add_item("Water Bottle", "Empty", 1, "hydration")

    results = manager.search_items("canned")
    assert len(results) == 2
    assert {item['name'] for item in results} == {"Canned Peaches", "Canned Tuna"}

def test_search_items_by_description(manager):
    """Test searching items by description."""
    manager.add_item("Old Map", "Torn, but useful", 1, "navigation")
    manager.add_item("Broken Radio", "Needs repair", 1, "electronics")

    results = manager.search_items("repair")
    assert len(results) == 1
    assert results[0]['name'] == "Broken Radio"

def test_search_items_by_tag(manager):
    """Test searching items by tag."""
    manager.add_item("First Aid Kit", "Basic supplies", 1, "medical, survival")
    manager.add_item("Painkillers", "For injuries", 10, "medical")
    manager.add_item("Rope", "Strong", 1, "utility")

    results = manager.search_items("medical")
    assert len(results) == 2
    assert {item['name'] for item in results} == {"First Aid Kit", "Painkillers"}

def test_search_items_no_match(manager):
    """Test searching for items that don't exist."""
    manager.add_item("Knife", "Sharp", 1, "weapon")
    results = manager.search_items("backpack")
    assert len(results) == 0

def test_remove_item(manager):
    """Test removing an item by ID."""
    manager.add_item("Matches", "Waterproof", 1, "fire") # ID 1
    manager.add_item("Compass", "Reliable", 1, "navigation") # ID 2
    manager.add_item("Tent", "Small", 1, "shelter") # ID 3

    assert manager.remove_item(2) is True
    assert len(manager.items) == 2
    assert manager.items[0]['name'] == "Matches"
    assert manager.items[1]['name'] == "Tent"

    assert manager.remove_item(99) is False # Non-existent ID
    assert len(manager.items) == 2 # Length should not change

def test_save_manifest(manager, temp_manifest_file):
    """Test saving the manifest to a file."""
    manager.add_item("Food Ration", "Emergency supply", 5, "food")
    manager.save_manifest()

    assert temp_manifest_file.exists()
    loaded_data = json.loads(temp_manifest_file.read_text())
    assert len(loaded_data) == 1
    assert loaded_data[0]['name'] == "Food Ration"

def test_load_manifest_manual(manager, temp_manifest_file):
    """Test manually loading the manifest from a file."""
    manager.add_item("Temporary Item", "Will be overwritten", 1, "temp")
    manager.save_manifest() # Save initial state

    # Now, simulate an external change or a fresh load
    external_data = [
        {"id": 1, "name": "New Item", "description": "Loaded", "quantity": 1, "tags": ["new"], "added_date": "2023-10-27T10:00:00"}
    ]
    temp_manifest_file.write_text(json.dumps(external_data))

    # Manually load
    manager._load_manifest() # Call the internal method directly for testing
    assert len(manager.items) == 1
    assert manager.items[0]['name'] == "New Item"
    assert manager._next_id == 2 # Should update _next_id based on loaded data

def test_tags_are_lowercase_and_stripped(manager):
    """Test that tags are processed correctly (lowercase, stripped)."""
    item = manager.add_item("Book", "Survival Guide", 1, "  Reading ,  KNOWLEDGE ")
    assert "reading" in item['tags']
    assert "knowledge" in item['tags']
    assert "  Reading " not in item['tags'] # Ensure stripping worked
    assert "KNOWLEDGE " not in item['tags'] # Ensure stripping worked
    assert len(item['tags']) == 2

def test_empty_tags(manager):
    """Test adding an item with empty tags."""
    item = manager.add_item("Empty Can", "Just a can", 1, "")
    assert item['tags'] == []

    item_no_tags = manager.add_item("Rock", "Heavy", 1, None)
    assert item_no_tags['tags'] == []
