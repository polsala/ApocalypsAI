import pytest
from unittest.mock import patch
from io import StringIO
import argparse
import sys

from src.checklist_generator import generate_apocalypse_checklist, main

# Mock rationale: The utility's core logic is pure function based on inputs.
# We don't need to mock external services or file system for `generate_apocalypse_checklist`.
# For `main`, we mock `argparse` to simulate CLI arguments and `sys.stdout`/`sys.stderr` to capture printed output,
# and `sys.exit` to prevent the test runner from terminating.

def test_generate_apocalypse_checklist_zombie_urban_moderate():
    scenario = "zombie_outbreak"
    location = "urban"
    resources = "moderate"
    checklist = generate_apocalypse_checklist(scenario, location, resources)

    assert "# Apocalypse Survival Checklist: Zombie Outbreak (Urban, Moderate Resources)" in checklist
    assert "## Immediate Actions:" in checklist
    assert "*   Secure your dwelling: Barricade doors and windows with heavy furniture." in checklist
    assert "*   Ensure all entry points are sealed against the undead." in checklist # Scenario specific
    assert "## Resource Adjustments (Moderate):" in checklist
    assert "*   You have some existing supplies; focus on replenishing and diversifying." in checklist
    assert "## Location Specifics (Urban):" in checklist
    assert "*   High population density means more immediate threats but also more potential resources." in checklist
    assert "*Stay vigilant, stay safe, and may your aim be true!" in checklist

def test_generate_apocalypse_checklist_meteor_rural_abundant():
    scenario = "meteor_strike"
    location = "rural"
    resources = "abundant"
    checklist = generate_apocalypse_checklist(scenario, location, resources)

    assert "# Apocalypse Survival Checklist: Meteor Strike (Rural, Abundant Resources)" in checklist
    assert "*   Seek immediate shelter underground or in structurally sound buildings." in checklist # Scenario specific
    assert "*   Lower population density means fewer immediate threats but also fewer readily available resources." in checklist # Location specific
    assert "*   You are well-stocked; focus on security, long-term sustainability, and helping others (cautiously)." in checklist # Resources specific

def test_generate_apocalypse_checklist_ai_suburban_minimal():
    scenario = "ai_uprising"
    location = "suburban"
    resources = "minimal"
    checklist = generate_apocalypse_checklist(scenario, location, resources)

    assert "# Apocalypse Survival Checklist: Ai Uprising (Suburban, Minimal Resources)" in checklist
    assert "*   Disconnect from all networked devices; disable smart home tech." in checklist # Scenario specific
    assert "*   A mix of urban and rural challenges. Balance resource gathering with maintaining a low profile." in checklist # Location specific
    assert "*   You are starting with very little; scavenging and resourcefulness are paramount." in checklist # Resources specific

def test_generate_apocalypse_checklist_solar_flare_urban_minimal():
    scenario = "solar_flare"
    location = "urban"
    resources = "minimal"
    checklist = generate_apocalypse_checklist(scenario, location, resources)

    assert "# Apocalypse Survival Checklist: Solar Flare (Urban, Minimal Resources)" in checklist
    assert "*   Unplug all sensitive electronics immediately to prevent EMP damage." in checklist # Scenario specific
    assert "*   High population density means more immediate threats but also more potential resources." in checklist # Location specific
    assert "*   You are starting with very little; scavenging and resourcefulness are paramount." in checklist # Resources specific

def test_generate_apocalypse_checklist_invalid_scenario_raises_error():
    with pytest.raises(ValueError, match="Invalid scenario: invalid_doom"): # Mock rationale: Testing input validation.
        generate_apocalypse_checklist("invalid_doom", "urban", "moderate")

def test_generate_apocalypse_checklist_invalid_location_raises_error():
    with pytest.raises(ValueError, match="Invalid location: nowhere"): # Mock rationale: Testing input validation.
        generate_apocalypse_checklist("zombie_outbreak", "nowhere", "moderate")

def test_generate_apocalypse_checklist_invalid_resources_raises_error():
    with pytest.raises(ValueError, match="Invalid resources: infinite"): # Mock rationale: Testing input validation.
        generate_apocalypse_checklist("zombie_outbreak", "urban", "infinite")

@patch('argparse.ArgumentParser.parse_args')
@patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture stdout to verify printed output.
def test_main_function_valid_args(mock_stdout, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        scenario="zombie_outbreak",
        location="urban",
        resources="moderate"
    )

    main()

    output = mock_stdout.getvalue()
    assert "# Apocalypse Survival Checklist: Zombie Outbreak (Urban, Moderate Resources)" in output
    assert "## Immediate Actions:" in output
    assert "*Stay vigilant, stay safe, and may your aim be true!" in output

@patch('argparse.ArgumentParser.parse_args')
@patch('sys.stderr', new_callable=StringIO) # Mock rationale: Capture stderr for error messages.
@patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
def test_main_function_invalid_args_error_handling(mock_exit, mock_stderr, mock_parse_args):
    # Simulate argparse returning an argument that would cause a ValueError in generate_apocalypse_checklist
    mock_parse_args.return_value = argparse.Namespace(
        scenario="zombie_outbreak",
        location="invalid_location", # This value would normally be caught by argparse's choices, but we're testing the ValueError path within main.
        resources="moderate"
    )

    main()

    # Verify that sys.exit(1) was called
    mock_exit.assert_called_once_with(1)
    # Verify error message was printed to stderr
    error_output = mock_stderr.getvalue()
    assert "Error: Invalid location: invalid_location" in error_output
