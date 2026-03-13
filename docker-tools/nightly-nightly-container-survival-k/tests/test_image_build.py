import subprocess
import pytest

def test_docker_image_build():
    """Test that the Docker image builds successfully."""
    result = subprocess.run(["docker", "build", "./src", "-t", "survival-kit:test"], capture_output=True, text=True)
    assert result.returncode == 0, f"Build failed: {result.stderr}"

@pytest.mark.parametrize("tool", [
    "curl",
    "wget",
    "ping",
    "nslookup",
    "dig",
    "tcpdump",
    "strace",
    "htop",
    "vim",
])
def test_tool_installed(tool):
    """Test that essential tools are installed in the image."""
    result = subprocess.run(
        ["docker", "run", "--rm", "survival-kit:test", "which", tool],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Tool '{tool}' not found in image"

# Mock rationale: Actual Docker daemon interaction is mocked via controlled subprocess calls in CI environments.
