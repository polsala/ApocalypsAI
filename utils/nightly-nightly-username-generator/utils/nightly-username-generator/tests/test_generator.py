import re

from nightly_username_generator.generator import generate_username


def test_deterministic_same_seed():
    """Two calls with the same seed must produce identical usernames."""
    username_a = generate_username(seed=42)
    username_b = generate_username(seed=42)
    assert username_a == username_b, "Usernames differ for identical seed"


def test_different_seeds_produce_different_usernames():
    """Different seeds should (very likely) yield different usernames."""
    username_a = generate_username(seed=1)
    username_b = generate_username(seed=2)
    assert username_a != username_b, "Usernames unexpectedly identical for different seeds"


def test_username_pattern():
    """Generated usernames must match the expected regex pattern."""
    pattern = re.compile(r"^[a-z]+-[a-z]+\d{3}$")
    for seed in [None, 0, 7, 12345, 999999]:
        username = generate_username(seed=seed)
        assert pattern.match(username), f"Username '{username}' does not match pattern"

# Mock rationale: No external services are called; the generator is pure‑function.
# The tests are deterministic and run offline.
