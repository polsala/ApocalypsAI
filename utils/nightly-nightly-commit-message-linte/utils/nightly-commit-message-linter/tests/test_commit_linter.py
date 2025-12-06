import subprocess
import sys
from pathlib import Path

# Mock rationale: we invoke the module as a subprocess to capture exit codes and stdout.
# This ensures the CLI behaves exactly as a user would see it, without needing external files.

def run_linter(input_text: str) -> subprocess.CompletedProcess:
    """Run the linter with *input_text* piped via stdin.

    Returns the CompletedProcess object for inspection.
    """
    proc = subprocess.run(
        [sys.executable, "-m", "nightly_commit_message_linter"],
        input=input_text.encode("utf-8"),
        capture_output=True,
        cwd=Path(__file__).parents[2] / "src",
    )
    return proc


def test_valid_message():
    valid = "feat(parser): add new AST node\n\nDetailed body is optional."
    result = run_linter(valid)
    assert result.returncode == 0
    assert b"Commit message is valid" in result.stdout


def test_missing_type():
    invalid = "add new feature without type"
    result = run_linter(invalid)
    assert result.returncode == 1
    assert b"Subject does not match" in result.stdout


def test_uppercase_description():
    invalid = "fix: Uppercase description starts wrong"
    result = run_linter(invalid)
    assert result.returncode == 1
    assert b"Description should start with a lowercase" in result.stdout


def test_description_ends_with_period():
    invalid = "docs: update README."
    result = run_linter(invalid)
    assert result.returncode == 1
    assert b"Description should not end with a period" in result.stdout
