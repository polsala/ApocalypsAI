import pytest
from unittest.mock import patch
import sys
from io import StringIO

from src.checklist_generator import generate_checklist, list_scenarios, SCENARIOS, main

def test_generate_checklist_valid_scenario():
    # Test a valid scenario returns the correct checklist.
    scenario = "zombie-outbreak"
    checklist = generate_checklist(scenario)
    assert isinstance(checklist, list)
    assert len(checklist) > 0
    assert checklist == SCENARIOS[scenario]

def test_generate_checklist_invalid_scenario():
    # Test an invalid scenario raises a ValueError.
    scenario = "non-existent-apocalypse"
    with pytest.raises(ValueError, match=f"Unknown scenario: '{scenario}'"): # Mock rationale: Testing error handling for invalid input without external dependencies.
        generate_checklist(scenario)

def test_list_scenarios():
    # Test that list_scenarios returns a sorted list of scenario keys.
    scenarios = list_scenarios()
    assert isinstance(scenarios, list)
    assert len(scenarios) == len(SCENARIOS)
    assert scenarios == sorted(list(SCENARIOS.keys()))

def test_main_list_scenarios_output():
    # Test the CLI output when --list-scenarios is used.
    test_args = ['checklist_generator.py', '--list-scenarios']
    expected_output_lines = ["Available Scenarios:"] + [f"- {s}" for s in sorted(SCENARIOS.keys())]
    expected_output = "\n".join(expected_output_lines) + "\n"

    with patch.object(sys, 'argv', test_args): # Mock rationale: Simulating command-line arguments for CLI testing.
        with patch('sys.stdout', new=StringIO()) as mock_stdout: # Mock rationale: Capturing stdout to verify printed output.
            with pytest.raises(SystemExit) as cm: # Mock rationale: main() calls sys.exit(), which pytest catches as SystemExit.
                main()
            assert cm.value.code == 0 # Mock rationale: Expecting a successful exit code.
            assert mock_stdout.getvalue() == expected_output

def test_main_generate_checklist_output():
    # Test the CLI output when a valid --scenario is used.
    scenario = "ai-uprising"
    test_args = ['checklist_generator.py', '--scenario', scenario]
    expected_output_lines = [
        f"\n--- Apocalypse Prep Checklist for '{scenario}' ---"
    ] + [
        f"{i}. {item}" for i, item in enumerate(SCENARIOS[scenario], 1)
    ] + [
        "--------------------------------------------------"
    ]
    expected_output = "\n".join(expected_output_lines) + "\n"

    with patch.object(sys, 'argv', test_args): # Mock rationale: Simulating command-line arguments for CLI testing.
        with patch('sys.stdout', new=StringIO()) as mock_stdout: # Mock rationale: Capturing stdout to verify printed output.
            with pytest.raises(SystemExit) as cm: # Mock rationale: main() calls sys.exit(), which pytest catches as SystemExit.
                main()
            assert cm.value.code == 0 # Mock rationale: Expecting a successful exit code.
            assert mock_stdout.getvalue() == expected_output

def test_main_invalid_scenario_output():
    # Test the CLI output and exit code for an invalid scenario.
    scenario = "unknown-threat"
    test_args = ['checklist_generator.py', '--scenario', scenario]
    expected_error_output = f"Error: Unknown scenario: '{scenario}'. Use --list-scenarios to see options.\n"

    with patch.object(sys, 'argv', test_args): # Mock rationale: Simulating command-line arguments for CLI testing.
        with patch('sys.stderr', new=StringIO()) as mock_stderr: # Mock rationale: Capturing stderr to verify error messages.
            with pytest.raises(SystemExit) as cm: # Mock rationale: main() calls sys.exit(), which pytest catches as SystemExit.
                main()
            assert cm.value.code == 1 # Mock rationale: Expecting a failure exit code.
            assert mock_stderr.getvalue() == expected_error_output

def test_main_no_args_output():
    # Test the CLI output when no arguments are provided (should print help and exit with error).
    test_args = ['checklist_generator.py']

    with patch.object(sys, 'argv', test_args): # Mock rationale: Simulating command-line arguments for CLI testing.
        with patch('sys.stdout', new=StringIO()) as mock_stdout: # Mock rationale: Capturing stdout to verify printed help message.
            with pytest.raises(SystemExit) as cm: # Mock rationale: main() calls sys.exit(), which pytest catches as SystemExit.
                main()
            assert cm.value.code == 1 # Mock rationale: Expecting a failure exit code.
            # We don't assert the exact help message as it can vary slightly, just that it prints something and exits with 1.
            assert "usage: checklist_generator.py" in mock_stdout.getvalue()
