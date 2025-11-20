import pytest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO
import sys

# Assuming pytest is run from the utility's root directory (e.g., utils/nightly-rubble-rouser-resource-tracker/)
from src import tracker

# Mock the DATA_FILE path to ensure tests don't interfere with actual files.
# Mock rationale: We want to ensure tests are deterministic and don't create/modify
# actual files on the filesystem. By mocking `os.path.exists` and `open`, we
# control the file content directly in memory.
MOCK_DATA_FILE = 'mock_resources.json'
tracker.DATA_FILE = MOCK_DATA_FILE # This modifies a global variable in the module under test for isolation.

@pytest.fixture
def mock_filesystem():
    """Fixture to mock file operations for _load_resources and _save_resources."""
    mock_file_content = {}

    def mock_exists(path):
        # Mock rationale: Control whether the data file "exists" for _load_resources.
        return path == MOCK_DATA_FILE and bool(mock_file_content)

    def mock_open_func(path, mode='r', encoding=None):
        # Mock rationale: Intercept file read/write operations to use in-memory content.
        if path == MOCK_DATA_FILE:
            if 'w' in mode:
                m_open = mock_open()
                # Mock rationale: Capture the string data written to the file and parse it
                # to update the in-memory mock_file_content, simulating file persistence.
                def _write_side_effect(data):
                    nonlocal mock_file_content
                    mock_file_content = json.loads(data) # Replace content with new state
                m_open.return_value.write.side_effect = _write_side_effect
                return m_open.return_value
            elif 'r' in mode:
                # When reading, provide the current in-memory content
                m_open = mock_open(read_data=json.dumps(mock_file_content))
                return m_open.return_value
        # Fallback for other files, though not expected in this utility's context
        return open(path, mode, encoding)

    with patch('os.path.exists', side_effect=mock_exists),
         patch('builtins.open', side_effect=mock_open_func):
        yield mock_file_content # Yield the in-memory content for assertions

@pytest.fixture
def capsys_output(capsys):
    """Fixture to capture stdout and stderr."""
    # Mock rationale: Capture print statements to verify CLI output.
    return capsys

def test_add_resource_new_item(mock_filesystem, capsys_output):
    tracker.add_resource("Water Bottle", 10)
    assert mock_filesystem == {"Water Bottle": 10}
    captured = capsys_output.readouterr()
    assert "Added 10 of 'Water Bottle'. Current total: 10" in captured.out

def test_add_resource_existing_item(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 10})
    tracker.add_resource("Water Bottle", 5)
    assert mock_filesystem == {"Water Bottle": 15}
    captured = capsys_output.readouterr()
    assert "Added 5 of 'Water Bottle'. Current total: 15" in captured.out

def test_add_resource_invalid_quantity(mock_filesystem, capsys_output):
    tracker.add_resource("Food Rations", "abc")
    assert mock_filesystem == {} # Should not add anything
    captured = capsys_output.readouterr()
    assert "Quantity must be an integer." in captured.err

    tracker.add_resource("Food Rations", -5)
    assert mock_filesystem == {}
    captured = capsys_output.readouterr()
    assert "Quantity must be a positive integer." in captured.err

def test_list_resources_empty(mock_filesystem, capsys_output):
    tracker.list_resources()
    captured = capsys_output.readouterr()
    assert "Your stash is currently empty. Time to scavenge!" in captured.out

def test_list_resources_with_items(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 10, "Duct Tape": 2})
    tracker.list_resources()
    captured = capsys_output.readouterr()
    assert "--- Current Stash ---" in captured.out
    assert "- Duct Tape: 2" in captured.out
    assert "- Water Bottle: 10" in captured.out
    assert "---------------------" in captured.out

def test_consume_resource_success(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 10})
    tracker.consume_resource("Water Bottle", 3)
    assert mock_filesystem == {"Water Bottle": 7}
    captured = capsys_output.readouterr()
    assert "Consumed 3 of 'Water Bottle'. Remaining: 7" in captured.out

def test_consume_resource_remove_item(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 3})
    tracker.consume_resource("Water Bottle", 3)
    assert mock_filesystem == {}
    captured = capsys_output.readouterr()
    assert "Consumed all 3 of 'Water Bottle'. Item removed from stash." in captured.out

def test_consume_resource_not_found(mock_filesystem, capsys_output):
    tracker.consume_resource("NonExistentItem", 1)
    assert mock_filesystem == {}
    captured = capsys_output.readouterr()
    assert "'NonExistentItem' not found in your stash." in captured.err

def test_consume_resource_not_enough(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 5})
    tracker.consume_resource("Water Bottle", 10)
    assert mock_filesystem == {"Water Bottle": 5} # Should not change
    captured = capsys_output.readouterr()
    assert "Not enough 'Water Bottle' to consume. You only have 5." in captured.err

def test_consume_resource_invalid_quantity(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 5})
    tracker.consume_resource("Water Bottle", "abc")
    assert mock_filesystem == {"Water Bottle": 5}
    captured = capsys_output.readouterr()
    assert "Quantity must be an integer." in captured.err

    tracker.consume_resource("Water Bottle", -2)
    assert mock_filesystem == {"Water Bottle": 5}
    captured = capsys_output.readouterr()
    assert "Quantity to consume must be a positive integer." in captured.err

def test_clear_resources(mock_filesystem, capsys_output):
    mock_filesystem.update({"Water Bottle": 10, "Duct Tape": 2})
    tracker.clear_resources()
    assert mock_filesystem == {}
    captured = capsys_output.readouterr()
    assert "Stash cleared! Ready for a fresh start." in captured.out

# Test main function CLI parsing
@patch('sys.argv', ['tracker.py', 'add', 'Medkit', '3'])
def test_main_add(mock_filesystem, capsys_output):
    # Mock rationale: Simulate command-line arguments for the main function.
    tracker.main()
    assert mock_filesystem == {"Medkit": 3}
    captured = capsys_output.readouterr()
    assert "Added 3 of 'Medkit'. Current total: 3" in captured.out

@patch('sys.argv', ['tracker.py', 'list'])
def test_main_list(mock_filesystem, capsys_output):
    mock_filesystem.update({"Medkit": 3})
    tracker.main()
    captured = capsys_output.readouterr()
    assert "- Medkit: 3" in captured.out

@patch('sys.argv', ['tracker.py', 'consume', 'Medkit', '1'])
def test_main_consume(mock_filesystem, capsys_output):
    mock_filesystem.update({"Medkit": 3})
    tracker.main()
    assert mock_filesystem == {"Medkit": 2}
    captured = capsys_output.readouterr()
    assert "Consumed 1 of 'Medkit'. Remaining: 2" in captured.out

@patch('sys.argv', ['tracker.py', 'clear'])
def test_main_clear(mock_filesystem, capsys_output):
    mock_filesystem.update({"Medkit": 3})
    tracker.main()
    assert mock_filesystem == {}
    captured = capsys_output.readouterr()
    assert "Stash cleared! Ready for a fresh start." in captured.out

@patch('sys.argv', ['tracker.py', 'unknown_command'])
def test_main_unknown_command(mock_filesystem, capsys_output):
    with pytest.raises(SystemExit) as excinfo:
        tracker.main()
    assert excinfo.value.code == 1
    captured = capsys_output.readouterr()
    assert "Unknown command: unknown_command" in captured.err

@patch('sys.argv', ['tracker.py'])
def test_main_no_command(mock_filesystem, capsys_output):
    with pytest.raises(SystemExit) as excinfo:
        tracker.main()
    assert excinfo.value.code == 1
    captured = capsys_output.readouterr()
    assert "Usage: python tracker.py <command> [args...]" in captured.err

@patch('sys.argv', ['tracker.py', 'add', 'Item']) # Missing quantity
def test_main_add_missing_arg(mock_filesystem, capsys_output):
    with pytest.raises(SystemExit) as excinfo:
        tracker.main()
    assert excinfo.value.code == 1
    captured = capsys_output.readouterr()
    assert "Usage: python tracker.py add <item_name> <quantity>" in captured.err

@patch('sys.argv', ['tracker.py', 'consume', 'Item']) # Missing quantity
def test_main_consume_missing_arg(mock_filesystem, capsys_output):
    with pytest.raises(SystemExit) as excinfo:
        tracker.main()
    assert excinfo.value.code == 1
    captured = capsys_output.readouterr()
    assert "Usage: python tracker.py consume <item_name> <quantity>" in captured.err
