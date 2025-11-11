import pytest

# Mock rationale: No external resources are required; tests are deterministic and run offline.

from utils.git-branch-sanitizer.src.sanitizer import sanitize_branch_name

@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Feature/Add-User", "feature-add-user"),
        ("  Hot Fix  ", "hot-fix"),
        ("Release_v1.2.3", "release-v1-2-3"),
        ("My   Complex___Branch.Name", "my-complex-branch-name"),
        ("/Leading/Slash", "leading-slash"),
        ("Trailing/Slash/", "trailing-slash"),
        ("Multiple---Hyphens", "multiple-hyphens"),
        ("Special!@#$%^&*()Chars", "special-chars"),
        ("Already‑kebab-case", "already‑kebab-case"),  # note: non‑ASCII hyphen stays as is after lower‑casing
    ],
)
def test_sanitize_branch_name(raw, expected):
    assert sanitize_branch_name(raw) == expected
