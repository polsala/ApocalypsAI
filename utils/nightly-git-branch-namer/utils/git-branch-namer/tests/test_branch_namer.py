import pytest
from src.branch_namer import suggest_branch_name

# Mock rationale: the utility is pure‑Python and does not perform any I/O or network calls.
# Therefore no external mocking is required; the tests are fully deterministic.

def test_basic_conversion():
    msg = "Add support for user authentication"
    expected = "add-support-for-user"
    assert suggest_branch_name(msg) == expected

def test_truncation_by_word_limit():
    msg = "Refactor the payment processing module to improve performance and readability"
    # Only first 4 words are kept
    expected = "refactor-the-payment-processing"
    assert suggest_branch_name(msg) == expected

def test_truncation_by_length():
    msg = "Implement a very long feature name that exceeds the maximum allowed branch length"
    # After cleaning and taking up to 4 words we get a long candidate; it should be trimmed.
    result = suggest_branch_name(msg)
    assert len(result) <= 30
    # Ensure it still starts with a letter and contains hyphens only
    assert result[0].isalpha()
    assert "-" in result

def test_non_alpha_start():
    msg = "123 fix typo in docs"
    # The cleaned first word is "123" which is numeric; the function should prepend "branch-"
    expected = "branch-123-fix-typo"
    assert suggest_branch_name(msg) == expected

def test_empty_message_raises():
    with pytest.raises(ValueError):
        suggest_branch_name("!!! ***")
