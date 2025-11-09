import pytest
import random
from src.morale_booster import get_boost, MORALE_BOOSTS

def test_get_boost_returns_string():
    """
    Test that get_boost always returns a string.
    """
    boost = get_boost()
    assert isinstance(boost, str)
    assert len(boost) > 0

def test_get_boost_returns_from_list():
    """
    Test that the returned boost is one of the predefined messages.
    """
    boost = get_boost()
    assert boost in MORALE_BOOSTS

def test_get_boost_deterministic_with_seed():
    """
    Test that get_boost returns a deterministic message when a seed is provided.
    # Mock rationale: Using random.seed() directly makes the test deterministic
    # without needing to mock random.choice. This is simpler and more direct
    # for this specific use case.
    """
    # Test with a specific seed
    first_boost = get_boost(seed=42)
    second_boost = get_boost(seed=42)
    assert first_boost == second_boost
    assert first_boost == "Your code is the last bastion against chaos. No pressure, though." # Known output for seed 42

    # Test with a different seed
    third_boost = get_boost(seed=100)
    fourth_boost = get_boost(seed=100)
    assert third_boost == fourth_boost
    assert third_boost == "The apocalypse is just a refactoring opportunity. Keep calm and commit on." # Known output for seed 100

def test_get_boost_multiple_calls_different_without_seed():
    """
    Verify that without a seed, multiple calls are likely to be different.
    This isn't a strict guarantee but checks for obvious non-randomness.
    # Mock rationale: No mock needed. This test verifies the default random behavior.
    """
    boosts = [get_boost() for _ in range(10)]
    # Check if there's at least some variety. Given MORALE_BOOSTS has many items,
    # it's highly improbable that 10 random choices would all be the same.
    assert len(set(boosts)) > 1 or len(MORALE_BOOSTS) == 1
