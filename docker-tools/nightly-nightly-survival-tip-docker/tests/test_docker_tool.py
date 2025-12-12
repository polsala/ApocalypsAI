import unittest
from unittest import mock
import subprocess

def build_image(tag="survival-tip"):
    """Build the Docker image using the Docker CLI."""
    subprocess.run(["docker", "build", "-t", tag, "."], check=True)

def run_container(tag="survival-tip"):
    """Run the Docker container and capture its stdout."""
    result = subprocess.run(
        ["docker", "run", "--rm", tag],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

class TestSurvivalTipDocker(unittest.TestCase):
    @mock.patch("subprocess.run")
    def test_build_and_run(self, mock_run):
        # Mock the build command
        mock_run.return_value = mock.Mock(stdout="Successfully built", returncode=0)
        build_image()
        mock_run.assert_any_call(["docker", "build", "-t", "survival-tip", "."], check=True)

        # Mock the run command with a sample tip output
        mock_run.return_value = mock.Mock(stdout="Never trust a cactus with a secret.\n", returncode=0)
        output = run_container()
        mock_run.assert_any_call(["docker", "run", "--rm", "survival-tip"], capture_output=True, text=True, check=True)
        # Ensure the output is non‑empty (deterministic mock guarantees this)
        self.assertTrue(len(output) > 0)

if __name__ == "__main__":
    unittest.main()
