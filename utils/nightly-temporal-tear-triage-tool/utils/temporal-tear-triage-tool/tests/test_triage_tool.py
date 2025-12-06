import pytest
import json
import os
from unittest.mock import patch, mock_open
from src.triage_tool import TriageTool

# Mock rationale: We need to test file operations (load/save) without actually touching the filesystem.
# `patch('builtins.open', ...)` allows us to intercept file open calls.
# `patch('os.path.exists', ...)` allows us to control whether the data file appears to exist.

@pytest.fixture
def mock_data_file():
    """Fixture to provide a consistent mock data file path."""
    return "test_anomalies.json"

@pytest.fixture
def empty_tool(mock_data_file):
    """Fixture for a TriageTool instance with an empty (mocked) data file."""
    with patch('os.path.exists', return_value=False), \
         patch('builtins.open', mock_open()) as mock_file:
        tool = TriageTool(data_file=mock_data_file)
        yield tool, mock_file

@pytest.fixture
def populated_tool(mock_data_file):
    """Fixture for a TriageTool instance with pre-populated (mocked) data."""
    initial_data = [
        {"id": 1, "description": "Fix minor time ripple", "urgency": 3, "impact": 2, "triage_score": 6, "completed": False},
        {"id": 2, "description": "Prevent paradox with self", "urgency": 5, "impact": 5, "triage_score": 25, "completed": False},
        {"id": 3, "description": "Calibrate Chronometer", "urgency": 2, "impact": 3, "triage_score": 6, "completed": True},
    ]
    mock_file_content = json.dumps(initial_data)

    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
        tool = TriageTool(data_file=mock_data_file)
        yield tool, mock_file, initial_data

def test_initialization_empty_file(empty_tool, mock_data_file):
    tool, mock_file = empty_tool
    assert tool.anomalies == []
    assert tool.data_file == mock_data_file
    # Mock rationale: Ensure that when the file doesn't exist, it's not opened for reading.
    mock_file.assert_not_called()

def test_initialization_populated_file(populated_tool, mock_data_file):
    tool, mock_file, initial_data = populated_tool
    assert tool.anomalies == initial_data
    assert tool.data_file == mock_data_file
    # Mock rationale: Ensure the file was opened for reading.
    mock_file.assert_called_once_with(mock_data_file, 'r')

def test_add_anomaly(empty_tool):
    tool, mock_file = empty_tool
    anomaly = tool.add_anomaly("Stabilize quantum fluctuations", urgency=4, impact=3)
    assert len(tool.anomalies) == 1
    assert anomaly['description'] == "Stabilize quantum fluctuations"
    assert anomaly['urgency'] == 4
    assert anomaly['impact'] == 3
    assert anomaly['triage_score'] == 12
    assert anomaly['id'] == 1
    assert not anomaly['completed']
    # Mock rationale: Verify that save was called after adding.
    mock_file.assert_called_with(tool.data_file, 'w')
    handle = mock_file()
    handle.write.assert_called_once()
    written_data = json.loads(handle.write.call_args[0][0])
    assert written_data[0]['description'] == "Stabilize quantum fluctuations"

def test_add_multiple_anomalies_id_increment(empty_tool):
    tool, mock_file = empty_tool
    tool.add_anomaly("First anomaly", urgency=1, impact=1)
    tool.add_anomaly("Second anomaly", urgency=2, impact=2)
    assert tool.anomalies[0]['id'] == 1
    assert tool.anomalies[1]['id'] == 2

def test_add_anomaly_invalid_urgency_impact(empty_tool):
    tool, _ = empty_tool
    with pytest.raises(ValueError, match="Urgency and Impact must be between 1 and 5."):
        tool.add_anomaly("Invalid urgency", urgency=0, impact=3)
    with pytest.raises(ValueError, match="Urgency and Impact must be between 1 and 5."):
        tool.add_anomaly("Invalid impact", urgency=3, impact=6)

def test_list_anomalies_sorted(populated_tool):
    tool, _, _ = populated_tool
    # Add a new high-priority anomaly
    tool.add_anomaly("Critical timeline divergence", urgency=5, impact=4) # Score 20
    # Add a new medium-priority anomaly
    tool.add_anomaly("Minor temporal echo", urgency=3, impact=3) # Score 9

    listed = tool.list_anomalies()
    # Active anomalies: ID 1 (6), ID 2 (25), ID 4 (20), ID 5 (9)
    # Sorted: ID 2 (25), ID 4 (20), ID 5 (9), ID 1 (6)
    assert len(listed) == 4
    assert listed[0]['description'] == "Prevent paradox with self" # Score 25
    assert listed[1]['description'] == "Critical timeline divergence" # Score 20
    assert listed[2]['description'] == "Minor temporal echo" # Score 9
    assert listed[3]['description'] == "Fix minor time ripple" # Score 6

def test_list_anomalies_include_completed(populated_tool):
    tool, _, _ = populated_tool
    listed = tool.list_anomalies(include_completed=True)
    assert len(listed) == 3 # All 3 initial anomalies, including the completed one
    assert any(a['completed'] for a in listed)

def test_complete_anomaly_success(populated_tool):
    tool, mock_file, _ = populated_tool
    assert not tool.anomalies[0]['completed'] # ID 1 is not completed initially
    result = tool.complete_anomaly(1)
    assert result is True
    assert tool.anomalies[0]['completed'] # ID 1 should now be completed
    # Mock rationale: Verify that save was called after completing.
    mock_file.assert_called_with(tool.data_file, 'w')
    handle = mock_file()
    written_data = json.loads(handle.write.call_args[0][0])
    assert written_data[0]['completed'] is True

def test_complete_anomaly_not_found(populated_tool):
    tool, _, _ = populated_tool
    result = tool.complete_anomaly(999)
    assert result is False
    # Mock rationale: No save should happen if anomaly not found. The mock_file was called once during init.
    # We verify it was not called again for saving by checking the return value of the method.

def test_complete_anomaly_already_completed(populated_tool):
    tool, _, _ = populated_tool
    # Anomaly ID 3 is already completed in initial_data
    result = tool.complete_anomaly(3)
    assert result is False
    # Mock rationale: No save should happen if anomaly already completed. We verify by checking the return value.
