import importlib.util
import pathlib


def _load_enhancer_module():
    """Load the enhancer module without relying on package imports.

    # Mock rationale: Using importlib to avoid issues with hyphenated folder names.
    """
    module_path = pathlib.Path(__file__).resolve().parents[2] / "src" / "enhancer.py"
    spec = importlib.util.spec_from_file_location("enhancer", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


enhancer = _load_enhancer_module()


def test_enhance_message_cases():
    cases = [
        ("fix typo in README", "🐛 fix typo in README"),
        ("Add new feature X", "➕ Add new feature X"),
        ("remove deprecated API", "❌ remove deprecated API"),
        ("Refactor module Y", "♻️ Refactor module Y"),
        ("Update documentation", "🔄 Update documentation"),
        ("docs: improve README", "📝 docs: improve README"),
        ("test: add unit tests", "✅ test: add unit tests"),
        ("chore: bump version", "chore: bump version"),  # no matching keyword
    ]
    for input_msg, expected in cases:
        assert enhancer.enhance_message(input_msg) == expected
