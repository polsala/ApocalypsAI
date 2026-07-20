import subprocess
import sys
import os
from unittest import mock

# Add the src directory to sys.path so we can import the Flask app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from app import mix_quote

def test_mix_quote_deterministic():
    """Mock random.choice to always pick the first element, ensuring a predictable output."""
    with mock.patch("random.choice", side_effect=lambda seq: seq[0]):
        assert mix_quote() == "The only limit is your mind. as the sky cracks open."

def test_docker_build_and_run_mock():
    """Mock subprocess.run to simulate successful Docker build and run commands."""
    with mock.patch("subprocess.run") as mock_run:
        # Simulate a successful command (returncode 0)
        mock_run.return_value = mock.Mock(returncode=0, stdout=b"", stderr=b"")

        def build_and_run():
            subprocess.run(["docker", "build", "-t", "quote-mixer", "."], check=True)
            subprocess.run(["docker", "run", "-d", "-p", "8080:8080", "quote-mixer"], check=True)

        build_and_run()

        # Verify that both Docker commands were invoked
        assert mock_run.call_count == 2
        first_call_args = mock_run.call_args_list[0][0][0]
        second_call_args = mock_run.call_args_list[1][0][0]
        assert first_call_args[:2] == ["docker", "build"]
        assert second_call_args[:2] == ["docker", "run"]
