import json
import sys
from pathlib import Path
import tempfile

# Mock rationale: Use a temporary directory to avoid polluting the repository and to ensure deterministic, offline tests.

# Import the tracker module using importlib (relative import works because tests run from the utils/resource-tracker directory)
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from tracker import ResourceTracker


def test_add_and_list_resources():
    with tempfile.TemporaryDirectory() as td:
        storage = Path(td) / "resources.json"
        tracker = ResourceTracker(storage)
        # Initially empty
        assert tracker.list_resources() == {}
        # Add resources
        tracker.add_resource("food", 10)
        tracker.add_resource("water", 5)
        # Verify list
        expected = {"food": 10, "water": 5}
        assert tracker.list_resources() == expected
        # Verify persistence by creating a new instance
        new_tracker = ResourceTracker(storage)
        assert new_tracker.list_resources() == expected


def test_consume_resource_success_and_cleanup():
    with tempfile.TemporaryDirectory() as td:
        storage = Path(td) / "resources.json"
        tracker = ResourceTracker(storage)
        tracker.add_resource("ammo", 7)
        # Consume part of it
        tracker.consume_resource("ammo", 3)
        assert tracker.list_resources()["ammo"] == 4
        # Consume the rest, should remove the key
        tracker.consume_resource("ammo", 4)
        assert "ammo" not in tracker.list_resources()
        # Persistence check
        new_tracker = ResourceTracker(storage)
        assert new_tracker.list_resources() == {}


def test_consume_resource_errors():
    with tempfile.TemporaryDirectory() as td:
        storage = Path(td) / "resources.json"
        tracker = ResourceTracker(storage)
        tracker.add_resource("medicine", 2)
        # Consuming more than available raises ValueError
        try:
            tracker.consume_resource("medicine", 5)
        except ValueError as e:
            assert "Not enough" in str(e)
        else:
            assert False, "Expected ValueError when over‑consuming"
        # Consuming a non‑existent resource raises KeyError
        try:
            tracker.consume_resource("fuel", 1)
        except KeyError as e:
            assert "not found" in str(e)
        else:
            assert False, "Expected KeyError for unknown resource"


def test_invalid_amounts_raise():
    with tempfile.TemporaryDirectory() as td:
        storage = Path(td) / "resources.json"
        tracker = ResourceTracker(storage)
        # Adding zero or negative amount
        for func in (tracker.add_resource, tracker.consume_resource):
            try:
                func("food", 0)
            except ValueError as e:
                assert "must be positive" in str(e)
            else:
                assert False, "Expected ValueError for non‑positive amount"
            try:
                func("food", -3)
            except ValueError as e:
                assert "must be positive" in str(e)
            else:
                assert False, "Expected ValueError for negative amount"
