import pytest
from src.main import suggest_branch_name, _slugify


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Add user authentication", "add-user-authentication"),
        ("Fix   multiple   spaces", "fix-multiple-spaces"),
        ("  Leading and trailing  ", "leading-and-trailing"),
        ("Special!@#Chars$$%", "special-chars"),
        ("MixedCASE Input", "mixedcase-input"),
    ],
)
def test_slugify(input_text, expected):
    assert _slugify(input_text) == expected


def test_suggest_without_issue():
    desc = "Implement OAuth2 login"
    assert suggest_branch_name(desc) == "implement-oauth2-login"


def test_suggest_with_issue():
    desc = "Refactor payment module"
    issue = 123
    assert suggest_branch_name(desc, issue) == "123-refactor-payment-module"

# Mock rationale: No external services are called; all logic is pure and deterministic.
