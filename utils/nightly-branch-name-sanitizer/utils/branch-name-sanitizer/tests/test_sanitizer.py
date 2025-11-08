import importlib.util
import pathlib
import pytest


def _load_sanitizer_module():
    """Load the sanitizer module from the sibling src directory.
    # Mock rationale: deterministic pure function, no external imports.
    """
    src_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "sanitizer.py"
    spec = importlib.util.spec_from_file_location("sanitizer", src_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sanitizer():
    return _load_sanitizer_module()


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Feature: Add New UI!", "feature-add-new-ui"),
        ("  leading and trailing  ", "leading-and-trailing"),
        ("Multiple___Separators...Here", "multiple-separators-here"),
        ("UPPER_case-MIXED", "upper-case-mixed"),
        ("---Already--kebab---", "already-kebab"),
        ("Special#Chars$%^&*", "specialchars"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_sanitize_branch_name(sanitizer, raw, expected):
    # Mock rationale: deterministic pure function, no external state.
    assert sanitizer.sanitize_branch_name(raw) == expected
