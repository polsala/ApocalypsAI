import subprocess
import re
import os
import sys

def run_tip(seed: int) -> str:
    """Execute src/tip.sh with a given SEED and return its stdout."""
    env = os.environ.copy()
    env["SEED"] = str(seed)
    # Ensure the script is executable; use bash explicitly for portability
    result = subprocess.run(["bash", "src/tip.sh"], cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"tip.sh exited with code {result.returncode}")
    return result.stdout.strip()

def test_deterministic_output():
    """# Mock rationale: Use a fixed seed to guarantee deterministic selection.
    The test checks that the output matches the expected pattern: an emoji followed by a space and a non‑empty tip.
    """
    output = run_tip(0)
    # Regex for a single Unicode emoji (broad range) followed by a space and text
    pattern = r"^[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF]\s.+$"
    assert re.match(pattern, output), f"Output does not match expected format: {output}"

def test_multiple_seeds_produce_different_tips():
    """# Mock rationale: Verify that different seeds lead to different indices.
    This ensures the randomisation logic works while still being deterministic for the test.
    """
    out1 = run_tip(1)
    out2 = run_tip(2)
    assert out1 != out2, "Different seeds should produce different tips"
