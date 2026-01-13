import subprocess
import sys

def test_date_utils_js():
    # Check if node is available
    try:
        subprocess.run(['node', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Skip test if node not available
        return
    result = subprocess.run(['node', 'tests/test_date_utils.js'], capture_output=True, text=True)
    assert result.returncode == 0, f"JS tests failed: {result.stdout}
{result.stderr}"
