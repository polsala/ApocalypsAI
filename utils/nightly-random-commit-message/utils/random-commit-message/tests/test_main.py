import sys
import pathlib
from unittest import mock

def test_generate_message_deterministic():
    # Add src directory to sys.path so we can import the module directly
    src_dir = pathlib.Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src_dir))
    from main import generate_message

    # Mock rationale: deterministic output by fixing random.choice sequence
    choices = ["🚀", "add", "shiny", "pipeline"]
    with mock.patch("random.choice", side_effect=choices):
        msg = generate_message()
        assert msg == "🚀 Add shiny pipeline"
