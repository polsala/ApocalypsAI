import pytest
from unittest.mock import patch, mock_open
from datetime import date, timedelta
import sys
import io

# Mock rationale: We need to control the current date for deterministic expiry calculations.
# Mock rationale: We need to simulate file system access without creating actual files.
# Mock rationale: We need to capture stdout/stderr to assert on printed output.

# Import the functions to be tested
from src.snack_scheduler import load_config, parse_item, generate_report, main

# --- Test load_config function ---

def test_load_config_success():
    mock_yaml_content = """
    items:
      - name: 'Test Item'
        quantity: 1
        expiry_date: '2025-01-01'
    """
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as mock_file:
        config = load_config('dummy_path.yml')
        assert config == {'items': [{'name': 'Test Item', 'quantity': 1, 'expiry_date': '2025-01-01'}]}
        mock_file.assert_called_once_with('dummy_path.yml', 'r')

def test_load_config_file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(SystemExit) as excinfo:
            load_config('non_existent.yml')
        assert excinfo.value.code == 1

def test_load_config_invalid_yaml():
    mock_yaml_content = """
    items:
      - name: 'Test Item'
        quantity: 1
        expiry_date: '2025-01-01'
    invalid_yaml: [-
    """
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
        with pytest.raises(SystemExit) as excinfo:
            load_config('invalid.yml')
        assert excinfo.value.code == 1

# --- Test parse_item function ---

def test_parse_item_success():
    item_data = {'name': 'Test Item', 'quantity': 5, 'expiry_date': '2024-06-15'}
    parsed_item = parse_item(item_data)
    assert parsed_item == {'name': 'Test Item', 'quantity': 5, 'expiry_date': date(2024, 6, 15)}

def test_parse_item_missing_key():
    item_data = {'name': 'Test Item', 'quantity': 5}
    with pytest.raises(ValueError, match="Missing key in item data: 'expiry_date'"):
        parse_item(item_data)

def test_parse_item_invalid_quantity():
    item_data = {'name': 'Test Item', 'quantity': 'five', 'expiry_date': '2024-06-15'}
    with pytest.raises(ValueError, match="Invalid value in item data: invalid literal for int() with base 10: 'five'"):
        parse_item(item_data)

def test_parse_item_invalid_date_format():
    item_data = {'name': 'Test Item', 'quantity': 5, 'expiry_date': '15-06-2024'}
    with pytest.raises(ValueError, match="Invalid value in item data: time data '15-06-2024' does not match format '%Y-%m-%d'"):
        parse_item(item_data)

# --- Test generate_report function ---

@pytest.fixture
def sample_inventory():
    return {
        'items': [
            {'name': 'Expired Snack', 'quantity': 1, 'expiry_date': '2023-01-01'},
            {'name': 'Expiring Soon Snack', 'quantity': 2, 'expiry_date': '2024-01-20'},
            {'name': 'Healthy Snack', 'quantity': 3, 'expiry_date': '2025-01-01'},
            {'name': 'Another Expiring Soon', 'quantity': 4, 'expiry_date': '2024-01-10'},
            {'name': 'Invalid Item', 'quantity': 'X', 'expiry_date': '2025-01-01'} # This item will be skipped
        ]
    }

@patch('sys.stderr', new_callable=io.StringIO)
def test_generate_report_all_categories(mock_stderr, sample_inventory):
    # Mock rationale: Set a fixed 'today' for deterministic test results.
    mock_today = date(2024, 1, 5) # Jan 5, 2024
    warning_days = 30

    report = generate_report(sample_inventory, warning_days, current_date=mock_today)

    assert f"Apocalypse Snack Stash Report (Today: {mock_today.isoformat()})" in report
    assert "--- Expired Items (1) ---" in report
    assert "- Expired Snack (1 units) - Expired 1009 days (2023-01-01)" in report
    assert f"--- Expiring Soon (< {warning_days} days) (2) ---" in report
    assert "- Another Expiring Soon (4 units) - Expires in 5 days (2024-01-10)" in report
    assert "- Expiring Soon Snack (2 units) - Expires in 15 days (2024-01-20)" in report
    assert "--- Healthy Stash (1) ---" in report
    assert "- Healthy Snack (3 units) - Expires in 362 days (2025-01-01)" in report
    assert "--- Inventory Summary ---" in report
    assert "Total unique items: 4" in report # Only valid items are counted
    assert "Total units: 10" in report # Sums valid items: 1+2+3+4 = 10
    assert "Warning: Skipping invalid item entry: Invalid value in item data: invalid literal for int() with base 10: 'X'" in mock_stderr.getvalue()

@patch('sys.stderr', new_callable=io.StringIO)
def test_generate_report_empty_inventory(mock_stderr):
    mock_today = date(2024, 1, 1)
    inventory = {'items': []}
    report = generate_report(inventory, 30, current_date=mock_today)

    assert "--- Expired Items (0) ---" in report
    assert "No items in this category." in report
    assert "--- Expiring Soon (< 30 days) (0) ---" in report
    assert "--- Healthy Stash (0) ---" in report
    assert "Total unique items: 0" in report
    assert "Total units: 0" in report
    assert mock_stderr.getvalue() == ""

@patch('sys.stderr', new_callable=io.StringIO)
def test_generate_report_no_items_key(mock_stderr):
    mock_today = date(2024, 1, 1)
    inventory = {'other_key': 'value'}
    report = generate_report(inventory, 30, current_date=mock_today)

    assert "--- Expired Items (0) ---" in report
    assert "No items in this category." in report
    assert "Total unique items: 0" in report
    assert "Total units: 0" in report
    assert mock_stderr.getvalue() == ""

# --- Test main function ---

@patch('src.snack_scheduler.load_config')
@patch('src.snack_scheduler.generate_report')
@patch('builtins.print')
@patch('sys.argv', ['snack_scheduler.py', '--config', 'test_config.yml', '--warning-days', '10'])
def test_main_function_with_args(mock_print, mock_generate_report, mock_load_config):
    # Mock rationale: We don't want main to actually load files or print to console during this test.
    # Mock rationale: We control sys.argv to simulate command-line arguments.
    mock_load_config.return_value = {'items': []}
    mock_generate_report.return_value = "Mock Report Content"

    main()

    mock_load_config.assert_called_once_with('test_config.yml')
    mock_generate_report.assert_called_once_with({'items': []}, 10)
    mock_print.assert_called_once_with("Mock Report Content")

@patch('src.snack_scheduler.load_config', side_effect=SystemExit(1))
@patch('builtins.print')
@patch('sys.argv', ['snack_scheduler.py'])
def test_main_function_load_config_failure(mock_print, mock_load_config):
    # Mock rationale: Simulate a failure during config loading and ensure main exits gracefully.
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    mock_load_config.assert_called_once_with('snacks.yml')
    mock_print.assert_not_called()
