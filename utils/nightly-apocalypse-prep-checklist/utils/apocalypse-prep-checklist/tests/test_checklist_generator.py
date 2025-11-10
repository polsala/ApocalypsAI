import pytest
import json
from unittest.mock import mock_open, patch
from utils.apocalypse_prep_checklist.src.checklist_generator import load_scenarios, generate_checklist

# Mock rationale: We need to test the utility's logic without relying on actual file system access.
# Mocking `open` allows us to provide predefined JSON content as if it were read from a file,
# ensuring deterministic and offline test execution.

@pytest.fixture
def mock_scenarios_data():
    """Fixture for mock scenarios data."""
    return {
        "test-scenario": {
            "title": "Test Scenario Title",
            "description": "A description for the test scenario.",
            "items": [
                "Item 1 for test",
                "Item 2 for test"
            ]
        },
        "empty-scenario": {
            "title": "Empty Scenario",
            "description": "This scenario has no items.",
            "items": []
        },
        "malformed-scenario": {
            "title": "Malformed Scenario"
            # Missing 'items' key intentionally
        }
    }

@pytest.fixture
def mock_scenarios_json(mock_scenarios_data):
    """Fixture for mock scenarios JSON string."""
    return json.dumps(mock_scenarios_data)

def test_load_scenarios_success(mock_scenarios_json, mock_scenarios_data):
    """Tests successful loading of scenarios from a mock JSON file."""
    with patch('builtins.open', mock_open(read_data=mock_scenarios_json)) as m_open:
        scenarios = load_scenarios('dummy_path/scenarios.json')
        m_open.assert_called_once_with('dummy_path/scenarios.json', 'r', encoding='utf-8')
        assert scenarios == mock_scenarios_data

def test_load_scenarios_file_not_found():
    """Tests handling of FileNotFoundError during scenario loading."""
    with patch('builtins.open', side_effect=FileNotFoundError) as m_open,
         patch('sys.stderr') as mock_stderr,
         pytest.raises(SystemExit) as excinfo:
        load_scenarios('non_existent_path/scenarios.json')
        m_open.assert_called_once()
        assert excinfo.value.code == 1
        mock_stderr.write.assert_any_call("Error: Scenarios file not found at non_existent_path/scenarios.json\n")

def test_load_scenarios_json_decode_error():
    """Tests handling of JSONDecodeError during scenario loading."""
    with patch('builtins.open', mock_open(read_data='{invalid json')) as m_open,
         patch('sys.stderr') as mock_stderr,
         pytest.raises(SystemExit) as excinfo:
        load_scenarios('dummy_path/invalid.json')
        m_open.assert_called_once()
        assert excinfo.value.code == 1
        mock_stderr.write.assert_any_call("Error: Invalid JSON in dummy_path/invalid.json\n")

def test_generate_checklist_valid_scenario(mock_scenarios_data):
    """Tests checklist generation for a valid scenario."""
    expected_output = (
        "# Test Scenario Title\n\n"
        "A description for the test scenario.\n\n"
        "## Checklist:\n"
        "- [ ] Item 1 for test\n"
        "- [ ] Item 2 for test\n"
    )
    checklist = generate_checklist('test-scenario', mock_scenarios_data)
    assert checklist == expected_output

def test_generate_checklist_unknown_scenario(mock_scenarios_data):
    """Tests handling of an unknown scenario name."""
    expected_output = "Error: Scenario 'unknown-scenario' not found. Available scenarios: test-scenario, empty-scenario, malformed-scenario"
    checklist = generate_checklist('unknown-scenario', mock_scenarios_data)
    assert checklist == expected_output

def test_generate_checklist_empty_items_scenario(mock_scenarios_data):
    """Tests checklist generation for a scenario with no items."""
    expected_output = (
        "# Empty Scenario\n\n"
        "This scenario has no items.\n\n"
        "No items defined for this scenario.\n"
    )
    checklist = generate_checklist('empty-scenario', mock_scenarios_data)
    assert checklist == expected_output

def test_generate_checklist_malformed_scenario(mock_scenarios_data):
    """Tests checklist generation for a scenario missing the 'items' key."""
    expected_output = (
        "# Malformed Scenario\n\n"
        "No description provided.\n\n"
        "No items defined for this scenario.\n"
    )
    checklist = generate_checklist('malformed-scenario', mock_scenarios_data)
    assert checklist == expected_output
