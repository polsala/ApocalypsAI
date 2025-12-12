import pytest
from unittest.mock import patch

# Mock rationale: We need to mock random.random to control the outcome of corruption.
# This ensures deterministic tests for the corruption logic.

from src.relay import corrupt_message, TRANSMISSION_ERRORS

def test_corrupt_message_no_corruption():
    """Test that message is not corrupted when corruption_chance is 0."""
    message = "This is a test message."
    corruption_chance = 0.0
    # Mock random.random to always return a value less than 0.0 (e.g., 0.0 itself)
    with patch('random.random', return_value=0.0):
        result = corrupt_message(message, corruption_chance)
        assert result == message

def test_corrupt_message_always_corruption():
    """Test that message is always corrupted when corruption_chance is 1."""
    message = "Another test message."
    corruption_chance = 1.0
    # Mock random.random to always return a value greater than or equal to 1.0 (e.g., 1.0)
    with patch('random.random', return_value=1.0):
        result = corrupt_message(message, corruption_chance)
        assert result != message
        assert any(error in result for error in TRANSMISSION_ERRORS)

def test_corrupt_message_specific_error_selection():
    """Test that a specific error is chosen when random.random returns a predictable value."""
    message = "Specific test."
    corruption_chance = 1.0
    # Mock random.random to return a value that maps to the first error in the list
    # Assuming TRANSMISSION_ERRORS has at least one element.
    mock_error_index = 0
    # The actual value returned by random.random doesn't matter as much as its position
    # in the sequence if we were to mock random.choice directly. Here, we mock random.random
    # and rely on random.choice picking the first element.
    with patch('random.random', return_value=0.5), patch('random.choice', return_value=TRANSMISSION_ERRORS[mock_error_index]) as mock_choice:
        result = corrupt_message(message, corruption_chance)
        assert result == f"{message} {TRANSMISSION_ERRORS[mock_error_index]}"
        mock_choice.assert_called_once_with(TRANSMISSION_ERRORS)

def test_corrupt_message_no_error_if_chance_is_low():
    """Test that message is not corrupted if random.random is just above the chance."""
    message = "Low chance test."
    corruption_chance = 0.7
    # Mock random.random to return a value slightly higher than corruption_chance
    with patch('random.random', return_value=0.7000001):
        result = corrupt_message(message, corruption_chance)
        assert result == message

def test_corrupt_message_error_if_chance_is_high():
    """Test that message is corrupted if random.random is just below the chance."""
    message = "High chance test."
    corruption_chance = 0.7
    # Mock random.random to return a value slightly lower than corruption_chance
    with patch('random.random', return_value=0.6999999):
        result = corrupt_message(message, corruption_chance)
        assert result != message
        assert any(error in result for error in TRANSMISSION_ERRORS)
