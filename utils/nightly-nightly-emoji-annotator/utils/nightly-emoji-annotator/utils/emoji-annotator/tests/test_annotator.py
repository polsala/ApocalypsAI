import pathlib
import tempfile

# Mock rationale: import the library directly from the src package.
from src.annotator import annotate_text


def test_annotate_simple():
    input_text = "I love fire and rocket."
    expected = "I love❤️ fire🔥 and rocket🚀."
    assert annotate_text(input_text) == expected


def test_annotate_case_insensitive():
    input_text = "Success, WARNING, and Error!"
    expected = "Success✅, WARNING⚠️, and Error❌!"
    assert annotate_text(input_text) == expected


def test_cli_output(tmp_path: pathlib.Path, capsys):
    # Mock rationale: using a temporary file to avoid external I/O.
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Idea: build a star.")

    # Import the module as a script entry point.
    from src import annotator
    annotator.main([str(sample_file)])
    captured = capsys.readouterr()
    assert captured.out == "Idea💡: build a star⭐."
