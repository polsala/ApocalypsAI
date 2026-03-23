import pytest
from unittest.mock import Mock, patch
from collections import defaultdict
import os
from src.scavenger_sim import get_config, run_simulation

# Mock rationale: We need to control os.getenv for deterministic configuration.
@patch.dict(os.environ, {
    'SIMULATION_DAYS': '3',
    'ZONES': 'Zone A,Zone B',
    'RESOURCES_PER_ZONE': '2',
    'RESOURCE_TYPES': 'Item X,Item Y'
})
def test_get_config_custom_env():
    """Test that get_config correctly parses custom environment variables."""
    config = get_config()
    assert config['simulation_days'] == 3
    assert config['zones'] == ['Zone A', 'Zone B']
    assert config['resources_per_zone'] == 2
    assert config['resource_types'] == ['Item X', 'Item Y']

# Mock rationale: We need to control os.getenv for deterministic configuration.
@patch.dict(os.environ, {}, clear=True) # Clear environment to test defaults
def test_get_config_defaults():
    """Test that get_config uses default values when environment variables are not set."""
    config = get_config()
    assert config['simulation_days'] == 7
    assert config['zones'] == ['Ruined City', 'Abandoned Factory', 'Overgrown Forest']
    assert config['resources_per_zone'] == 5
    assert config['resource_types'] == ['Water', 'Food', 'Scrap Metal', 'Medical Supplies', 'Fuel']

# Mock rationale: We need to control os.getenv for deterministic configuration.
@patch.dict(os.environ, {
    'ZONES': '', # Empty zones
    'RESOURCE_TYPES': '' # Empty resource types
}, clear=False) # Don't clear other env vars
def test_get_config_empty_lists():
    """Test that get_config handles empty zone/resource type strings gracefully."""
    config = get_config()
    assert config['zones'] == ['Default Zone'] # Should fall back to default
    assert config['resource_types'] == ['Unknown Resource'] # Should fall back to default

def test_run_simulation_no_finds():
    """Test simulation where no resources are found."""
    config = {
        'simulation_days': 2,
        'zones': ['Zone A'],
        'resources_per_zone': 0, # Max resources per zone is 0
        'resource_types': ['Item X']
    }
    # Mock rationale: random_randint_func is mocked to always return 0, simulating no finds.
    mock_randint = Mock(return_value=0)
    output = run_simulation(config, random_randint_func=mock_randint)

    assert "--- Scavenger Bot Simulation Started (2 days) ---" in output
    assert "No resources found today. Tough luck!" in output
    assert "No resources were found during the entire simulation." in output
    assert mock_randint.call_count == config['simulation_days'] * len(config['zones']) # Called for each day/zone

def test_run_simulation_with_finds():
    """Test simulation where resources are consistently found."""
    config = {
        'simulation_days': 2,
        'zones': ['Zone A', 'Zone B'],
        'resources_per_zone': 1,
        'resource_types': ['Item X', 'Item Y']
    }
    # Mock rationale:
    # mock_randint is mocked to always return 1, simulating one resource found per zone.
    # mock_choice is mocked to alternate between 'Item X' and 'Item Y' for deterministic resource assignment.
    mock_randint = Mock(return_value=1)
    mock_choice = Mock(side_effect=['Item X', 'Item Y', 'Item X', 'Item Y']) # Day 1: X, Y. Day 2: X, Y.

    output = run_simulation(config, random_choice_func=mock_choice, random_randint_func=mock_randint)

    assert "--- Scavenger Bot Simulation Started (2 days) ---" in output
    assert "Day 1:" in output
    assert "  Found 1x Item X across zones." in output # 1 from Zone A
    assert "  Found 1x Item Y across zones." in output # 1 from Zone B
    assert "Day 2:" in output
    assert "  Found 1x Item X across zones." in output # 1 from Zone A
    assert "  Found 1x Item Y across zones." in output # 1 from Zone B
    assert "Total Resources Collected:" in output
    assert "- Item X: 2" in output # 1 from Day 1, 1 from Day 2
    assert "- Item Y: 2" in output # 1 from Day 1, 1 from Day 2
    assert mock_randint.call_count == config['simulation_days'] * len(config['zones'])
    assert mock_choice.call_count == config['simulation_days'] * len(config['zones']) * config['resources_per_zone'] # 2 days * 2 zones * 1 resource/zone

def test_run_simulation_mixed_finds():
    """Test simulation with varying resource finds."""
    config = {
        'simulation_days': 3,
        'zones': ['Zone A'],
        'resources_per_zone': 3,
        'resource_types': ['Gold', 'Silver']
    }
    # Mock rationale:
    # mock_randint simulates: Day 1 (2 finds), Day 2 (0 finds), Day 3 (1 find).
    # mock_choice simulates: Day 1 (Gold, Silver), Day 3 (Gold).
    mock_randint = Mock(side_effect=[2, 0, 1])
    mock_choice = Mock(side_effect=['Gold', 'Silver', 'Gold'])

    output = run_simulation(config, random_choice_func=mock_choice, random_randint_func=mock_randint)

    assert "Day 1:" in output
    assert "  Found 1x Gold across zones." in output # Mocked choice
    assert "  Found 1x Silver across zones." in output # Mocked choice
    assert "Day 2:" in output
    assert "No resources found today. Tough luck!" in output
    assert "Day 3:" in output
    assert "  Found 1x Gold across zones." in output # Mocked choice
    assert "Total Resources Collected:" in output
    assert "- Gold: 2" in output
    assert "- Silver: 1" in output
    assert mock_randint.call_count == config['simulation_days'] * len(config['zones'])
    assert mock_choice.call_count == 3 # 2 from Day 1, 1 from Day 3
