import pytest
from utils.deterministic-passphrase-generator.src.generator import generate_password


def test_generate_password_default_length():
    master = "test"
    pwd = generate_password(master)
    # Expected value computed via SHA-256 + base64url, truncated to 12 chars
    assert pwd == "n4bQgYhMfWma"


def test_generate_password_custom_length():
    master = "test"
    pwd = generate_password(master, length=20)
    # First 20 chars of the same base64url string
    assert pwd == "n4bQgYhMfWmaL-qgxVrQ"


def test_generate_password_invalid_length():
    with pytest.raises(ValueError):
        generate_password("test", length=0)
