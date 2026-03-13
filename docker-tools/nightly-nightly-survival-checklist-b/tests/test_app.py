import json
import os
import importlib.util
import sys
import pytest

# Dynamically import the app module from src/app.py
spec = importlib.util.spec_from_file_location(
    "app", os.path.join(os.path.dirname(__file__), "..", "src", "app.py")
)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

def test_prioritize():
    items = [
        {"name": "Water", "importance": 10, "quantity": 5},
        {"name": "Canned Beans", "importance": 6, "quantity": 12},
        {"name": "First Aid Kit", "importance": 9, "quantity": 1},
        {"name": "Bandages", "importance": 9, "quantity": 3},
    ]
    result = app.prioritize(items)
    # Expected order: Water (10), Bandages (9, qty 3), First Aid Kit (9, qty 1), Canned Beans (6)
    assert result[0]["name"] == "Water"
    assert result[1]["name"] == "Bandages"
    assert result[2]["name"] == "First Aid Kit"
    assert result[3]["name"] == "Canned Beans"

def test_format_checklist():
    items = [
        {"name": "Water", "importance": 10, "quantity": 5},
        {"name": "Bandages", "importance": 9, "quantity": 3},
    ]
    output = app.format_checklist(items)
    expected = "1. Water (Qty: 5) - Importance: 10\n2. Bandages (Qty: 3) - Importance: 9"
    assert output == expected

def test_main_success(tmp_path, capsys):
    # Create a temporary supplies.json file
    data = {
        "items": [
            {"name": "Water", "importance": 10, "quantity": 5},
            {"name": "Canned Beans", "importance": 6, "quantity": 12},
        ]
    }
    (tmp_path / "supplies.json").write_text(json.dumps(data))
    # Change working directory to the temp path
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        app.main()
    finally:
        os.chdir(old_cwd)
    captured = capsys.readouterr()
    expected = "1. Water (Qty: 5) - Importance: 10\n2. Canned Beans (Qty: 12) - Importance: 6"
    assert captured.out.strip() == expected

def test_main_missing_file(tmp_path, capsys):
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(SystemExit) as excinfo:
            app.main()
        assert excinfo.value.code == 1
    finally:
        os.chdir(old_cwd)
    captured = capsys.readouterr()
    assert "Error: supplies.json not found" in captured.err
