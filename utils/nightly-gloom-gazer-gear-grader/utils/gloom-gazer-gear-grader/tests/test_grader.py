import pytest
import json
from unittest.mock import patch, mock_open
import io # Needed for sys.stdout/stderr mocking
from src.grader import load_json_file, get_default_rules, grade_item, main

# Mock rationale: We need to test file loading without actual file system access.
# `mock_open` simulates `open()` and `patch('os.path.exists')` simulates file existence checks.

@pytest.fixture
def mock_items_data():
    return [
        {
            "name": "Rusty Crowbar",
            "type": "weapon",
            "condition": "damaged",
            "rarity": "common",
            "weight_kg": 2.5
        },
        {
            "name": "Sealed MRE (Beef Stew)",
            "type": "food",
            "condition": "new",
            "rarity": "uncommon",
            "weight_kg": 0.4
        },
        {
            "name": "Medical Kit",
            "type": "medicine",
            "condition": "new",
            "rarity": "rare",
            "weight_kg": 1.0
        },
        {
            "name": "Broken Radio",
            "type": "tool",
            "condition": "broken",
            "rarity": "common",
            "weight_kg": 0.8
        },
        {
            "name": "Heavy Armor Plate",
            "type": "clothing",
            "condition": "used",
            "rarity": "uncommon",
            "weight_kg": 6.0
        },
        {
            "name": "Shiny Rock",
            "type": "junk",
            "condition": "new",
            "rarity": "common",
            "weight_kg": 0.1
        },
        {
            "name": "Legendary Plasma Rifle",
            "type": "weapon",
            "condition": "new",
            "rarity": "legendary",
            "weight_kg": 4.0
        }
    ]

@pytest.fixture
def mock_rules_data():
    return {
        "type_scores": {
            "weapon": 10,
            "tool": 8,
            "food": 7,
            "medicine": 12,
            "clothing": 5,
            "junk": -5
        },
        "condition_scores": {
            "new": 5,
            "used": 2,
            "damaged": -3,
            "broken": -10
        },
        "rarity_scores": {
            "rare": 10,
            "uncommon": 5,
            "common": 1,
            "legendary": 20
        },
        "weight_penalties": [
            {"threshold": 5, "penalty": -2},
            {"threshold": 10, "penalty": -5}
        ],
        "missing_attribute_penalty": -1
    }

def test_load_json_file_success(mock_items_data):
    # Mock rationale: Simulate a file existing and containing valid JSON.
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_items_data))) as mock_file:
        with patch('os.path.exists', return_value=True):
            data = load_json_file('dummy_path.json')
            assert data == mock_items_data
            mock_file.assert_called_once_with('dummy_path.json', 'r', encoding='utf-8')

def test_load_json_file_not_found():
    # Mock rationale: Simulate a file not existing.
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            load_json_file('non_existent.json')

def test_load_json_file_invalid_json():
    # Mock rationale: Simulate a file containing malformed JSON.
    with patch('builtins.open', mock_open(read_data='{invalid json')):
        with patch('os.path.exists', return_value=True):
            with pytest.raises(json.JSONDecodeError):
                load_json_file('malformed.json')

def test_get_default_rules():
    rules = get_default_rules()
    assert isinstance(rules, dict)
    assert 'type_scores' in rules
    assert 'condition_scores' in rules

def test_grade_item_basic(mock_rules_data):
    item = {"name": "Basic Tool", "type": "tool", "condition": "used", "rarity": "common", "weight_kg": 1.0}
    graded_item = grade_item(item, mock_rules_data)
    # Expected: type (tool=8) + condition (used=2) + rarity (common=1) + weight (0.0 < 5kg = 0) = 11
    assert graded_item['survival_score'] == 11

def test_grade_item_heavy_penalty(mock_rules_data):
    item = {"name": "Very Heavy Item", "type": "junk", "condition": "new", "rarity": "rare", "weight_kg": 7.0}
    graded_item = grade_item(item, mock_rules_data)
    # Expected: type (junk=-5) + condition (new=5) + rarity (rare=10) + weight (7kg >= 5kg = -2) = 8
    assert graded_item['survival_score'] == 8

def test_grade_item_missing_attributes(mock_rules_data):
    item = {"name": "Mystery Item"}
    graded_item = grade_item(item, mock_rules_data)
    # Expected: type (missing=-1) + condition (missing=-1) + rarity (missing=-1) + weight (0kg = 0) = -3
    assert graded_item['survival_score'] == -3

def test_grade_item_all_attributes(mock_rules_data):
    item = {"name": "Legendary Plasma Rifle", "type": "weapon", "condition": "new", "rarity": "legendary", "weight_kg": 4.0}
    graded_item = grade_item(item, mock_rules_data)
    # Expected: type (weapon=10) + condition (new=5) + rarity (legendary=20) + weight (4kg < 5kg = 0) = 35
    assert graded_item['survival_score'] == 35

def test_main_success(mock_items_data, mock_rules_data):
    # Mock rationale: Simulate command-line arguments, file existence, and file content.
    # Also capture stdout to verify the output.
    mock_items_json = json.dumps(mock_items_data)
    mock_rules_json = json.dumps(mock_rules_data)

    with patch('sys.argv', ['grader.py', '--items', 'items.json', '--rules', 'rules.json']),
         patch('os.path.exists', side_effect=lambda x: x in ['items.json', 'rules.json']),
         patch('builtins.open', side_effect=lambda f, mode, encoding: mock_open(read_data=mock_items_json if f == 'items.json' else mock_rules_json)(f, mode, encoding)),
         patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
         patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
        main()
        output = json.loads(mock_stdout.getvalue())
        assert isinstance(output, list)
        assert len(output) == len(mock_items_data)
        # Verify sorting (highest score first)
        assert output[0]['name'] == 'Legendary Plasma Rifle'
        assert output[0]['survival_score'] == 35
        assert output[-1]['name'] == 'Broken Radio'
        assert output[-1]['survival_score'] == -1
        assert mock_stderr.getvalue() == ""

def test_main_items_file_not_found():
    # Mock rationale: Simulate items file not existing.
    with patch('sys.argv', ['grader.py', '--items', 'non_existent.json']),
         patch('os.path.exists', return_value=False),
         patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
         patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
         pytest.raises(SystemExit) as excinfo:
        main()
        assert excinfo.value.code == 1
        assert "Error: File not found: non_existent.json" in mock_stderr.getvalue()

def test_main_invalid_items_json():
    # Mock rationale: Simulate items file containing invalid JSON.
    with patch('sys.argv', ['grader.py', '--items', 'malformed.json']),
         patch('os.path.exists', return_value=True),
         patch('builtins.open', mock_open(read_data='{invalid json')) as mock_file,
         patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
         patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
         pytest.raises(SystemExit) as excinfo:
        main()
        assert excinfo.value.code == 1
        assert "Error: Invalid JSON in file 'malformed.json'" in mock_stderr.getvalue()

def test_main_items_not_list():
    # Mock rationale: Simulate items file containing a JSON object, not a list.
    with patch('sys.argv', ['grader.py', '--items', 'not_list.json']),
         patch('os.path.exists', return_value=True),
         patch('builtins.open', mock_open(read_data='{"item": "data"}')) as mock_file,
         patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
         patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
         pytest.raises(SystemExit) as excinfo:
        main()
        assert excinfo.value.code == 1
        assert "Error: Items file must contain a JSON array of items." in mock_stderr.getvalue()

def test_main_default_rules(mock_items_data):
    # Mock rationale: Test main function using default internal rules when --rules is not provided.
    mock_items_json = json.dumps(mock_items_data)

    with patch('sys.argv', ['grader.py', '--items', 'items.json']),
         patch('os.path.exists', side_effect=lambda x: x == 'items.json'),
         patch('builtins.open', side_effect=lambda f, mode, encoding: mock_open(read_data=mock_items_json)(f, mode, encoding)),
         patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
         patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
        main()
        output = json.loads(mock_stdout.getvalue())
        assert isinstance(output, list)
        assert len(output) == len(mock_items_data)
        assert output[0]['name'] == 'Legendary Plasma Rifle'
        assert output[0]['survival_score'] == 35
        assert output[-1]['name'] == 'Broken Radio'
        assert output[-1]['survival_score'] == -1
        assert mock_stderr.getvalue() == ""
