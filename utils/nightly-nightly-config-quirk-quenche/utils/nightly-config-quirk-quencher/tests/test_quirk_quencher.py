import pytest
import sys
import os
import io
from unittest.mock import mock_open, patch
from src.quirk_quencher import validate_json, validate_yaml, validate_ini, main

# Mock rationale: We need to simulate file system interactions and file content
# without actually creating files or relying on the real file system,
# ensuring deterministic and offline tests.

@pytest.fixture
def mock_file_content():
    """Fixture to provide mock file content for various formats."""
    return {
        "valid_json": '{"name": "ApocalypsAI", "version": 1.0, "active": true}',
        "invalid_json": '{"name": "ApocalypsAI", "version": 1.0, "active": true,}', # Trailing comma
        "valid_yaml": 'name: ApocalypsAI\nversion: 1.0\nactive: true',
        "invalid_yaml": 'name: ApocalypsAI\n  version: 1.0\nactive: true', # Indentation error
        "valid_ini": '[General]\nname = ApocalypsAI\nversion = 1.0\n[Settings]\nactive = true',
        "invalid_ini": '[General\nname = ApocalypsAI', # Missing closing bracket
        "empty_file": '',
    }

@patch('os.path.exists', return_value=True) # Mock rationale: Simulate file existence for main function
def test_validate_json_valid(mock_exists, mock_file_content):
    """Test valid JSON file validation."""
    m_open = mock_open(read_data=mock_file_content["valid_json"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_json("dummy.json")
        assert is_valid is True
        assert "JSON file is valid." in message

@patch('os.path.exists', return_value=True)
def test_validate_json_invalid(mock_exists, mock_file_content):
    """Test invalid JSON file validation."""
    m_open = mock_open(read_data=mock_file_content["invalid_json"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_json("dummy.json")
        assert is_valid is False
        assert "Invalid JSON:" in message

@patch('os.path.exists', return_value=False)
def test_validate_json_file_not_found(mock_exists):
    """Test JSON validation with a non-existent file."""
    is_valid, message = validate_json("non_existent.json")
    assert is_valid is False
    assert "File not found:" in message

@patch('os.path.exists', return_value=True)
def test_validate_yaml_valid(mock_exists, mock_file_content):
    """Test valid YAML file validation."""
    m_open = mock_open(read_data=mock_file_content["valid_yaml"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_yaml("dummy.yaml")
        assert is_valid is True
        assert "YAML file is valid." in message

@patch('os.path.exists', return_value=True)
def test_validate_yaml_invalid(mock_exists, mock_file_content):
    """Test invalid YAML file validation."""
    m_open = mock_open(read_data=mock_file_content["invalid_yaml"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_yaml("dummy.yaml")
        assert is_valid is False
        assert "Invalid YAML:" in message

@patch('os.path.exists', return_value=False)
def test_validate_yaml_file_not_found(mock_exists):
    """Test YAML validation with a non-existent file."""
    is_valid, message = validate_yaml("non_existent.yaml")
    assert is_valid is False
    assert "File not found:" in message

@patch('os.path.exists', return_value=True)
def test_validate_ini_valid(mock_exists, mock_file_content):
    """Test valid INI file validation."""
    m_open = mock_open(read_data=mock_file_content["valid_ini"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_ini("dummy.ini")
        assert is_valid is True
        assert "INI file is valid." in message

@patch('os.path.exists', return_value=True)
def test_validate_ini_invalid(mock_exists, mock_file_content):
    """Test invalid INI file validation."""
    m_open = mock_open(read_data=mock_file_content["invalid_ini"])
    with patch('builtins.open', m_open):
        is_valid, message = validate_ini("dummy.ini")
        assert is_valid is False
        assert "Invalid INI:" in message

@patch('os.path.exists', return_value=False)
def test_validate_ini_file_not_found(mock_exists):
    """Test INI validation with a non-existent file."""
    is_valid, message = validate_ini("non_existent.ini")
    assert is_valid is False
    assert "File not found:" in message

@patch('os.path.exists', return_value=True)
def test_validate_empty_file(mock_exists, mock_file_content):
    """Test validation with an empty file for all types."""
    m_open = mock_open(read_data=mock_file_content["empty_file"])
    with patch('builtins.open', m_open):
        # JSON: empty string is not valid JSON
        is_valid, message = validate_json("empty.json")
        assert is_valid is False
        assert "Invalid JSON:" in message

        # YAML: empty string is valid YAML (represents null)
        is_valid, message = validate_yaml("empty.yaml")
        assert is_valid is True
        assert "YAML file is valid." in message

        # INI: empty string is valid INI (no sections/keys)
        is_valid, message = validate_ini("empty.ini")
        assert is_valid is True
        assert "INI file is valid." in message

# --- Test main function ---

@patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout for assertion
@patch('sys.stderr', new_callable=io.StringIO) # Mock rationale: Capture stderr for assertion
@patch('os.path.exists', return_value=True) # Mock rationale: Simulate file existence
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}') # Mock rationale: Simulate file content
def test_main_json_valid(mock_open_file, mock_exists, mock_stderr, mock_stdout):
    """Test main function with valid JSON."""
    test_args = ["quirk_quencher.py", "--file", "config.json", "--type", "json"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as cm: # Mock rationale: main() calls sys.exit()
            main()
        assert cm.value.code == 0
        assert "✅ Success: JSON file is valid." in mock_stdout.getvalue()
        assert not mock_stderr.getvalue()

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stderr', new_callable=io.StringIO)
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value",}') # Invalid JSON
def test_main_json_invalid(mock_open_file, mock_exists, mock_stderr, mock_stdout):
    """Test main function with invalid JSON."""
    test_args = ["quirk_quencher.py", "--file", "config.json", "--type", "json"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 1
        assert "❌ Failure: Invalid JSON:" in mock_stderr.getvalue()
        assert not mock_stdout.getvalue()

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stderr', new_callable=io.StringIO)
@patch('os.path.exists', return_value=False) # File does not exist
def test_main_file_not_found(mock_exists, mock_stderr, mock_stdout):
    """Test main function when file does not exist."""
    test_args = ["quirk_quencher.py", "--file", "non_existent.json", "--type", "json"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 1
        assert "Error: File not found at 'non_existent.json'" in mock_stderr.getvalue()
        assert not mock_stdout.getvalue()

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stderr', new_callable=io.StringIO)
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='name: value\n  key: value') # Invalid YAML
def test_main_yaml_invalid(mock_open_file, mock_exists, mock_stderr, mock_stdout):
    """Test main function with invalid YAML."""
    test_args = ["quirk_quencher.py", "--file", "config.yaml", "--type", "yaml"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 1
        assert "❌ Failure: Invalid YAML:" in mock_stderr.getvalue()

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stderr', new_callable=io.StringIO)
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='[Section]\nKey=Value') # Valid INI
def test_main_ini_valid(mock_open_file, mock_exists, mock_stderr, mock_stdout):
    """Test main function with valid INI."""
    test_args = ["quirk_quencher.py", "--file", "config.ini", "--type", "ini"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 0
        assert "✅ Success: INI file is valid." in mock_stdout.getvalue()
