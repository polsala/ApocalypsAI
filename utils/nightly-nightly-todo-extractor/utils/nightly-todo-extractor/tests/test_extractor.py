import sys
from pathlib import Path
import tempfile
import shutil

# Mock rationale: we use temporary directories/files to avoid any external I/O.
# This ensures the test suite is deterministic and runs offline.

# Import the utility under test.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
from extractor import extract_todos, generate_markdown


def create_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_extract_todos_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        # Create a Python file with various comments.
        py_file = root / "example.py"
        create_file(
            py_file,
            """
# TODO: Refactor this function
def foo():
    pass  # FIXME: remove placeholder

# This is a normal comment.
""",
        )
        # Create a JavaScript file.
        js_file = root / "script.js"
        create_file(
            js_file,
            """
// TODO implement feature X
function bar() {
    // FIXME: handle edge case
}
""",
        )
        report = extract_todos(root)
        # Expected keys are relative paths.
        assert Path("example.py") in report
        assert Path("script.js") in report
        # Verify counts.
        assert len(report[Path("example.py")]) == 2
        assert len(report[Path("script.js")]) == 2
        # Verify content of one entry.
        line_no, comment = report[Path("example.py")][0]
        assert line_no == 2  # line numbers are 1‑based
        assert comment == "Refactor this function"


def test_generate_markdown_empty():
    md = generate_markdown({})
    assert "_No TODO/FIXME comments found_" in md


def test_generate_markdown_content():
    report = {
        Path("a.py"): [(10, "Refactor this"), (20, "Fix bug")],
        Path("b.js"): [(5, "Add tests")],
    }
    md = generate_markdown(report)
    # Header and table rows should appear.
    assert "# TODO Report" in md
    assert "| `a.py` | 10 | Refactor this |" in md
    assert "| `b.js` | 5 | Add tests |" in md
