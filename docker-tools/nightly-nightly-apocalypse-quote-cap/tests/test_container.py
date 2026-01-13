import unittest
from unittest import mock
import subprocess
import json
import base64

def build_image():
    subprocess.run(["docker", "build", "-t", "quote-capsule:latest", "."], check=True)

def run_container(input_text, decode=False):
    cmd = ["docker", "run", "-i", "quote-capsule:latest"]
    if decode:
        cmd.append("--decode")
    result = subprocess.run(
        cmd,
        input=input_text.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode()

class TestQuoteCapsuleContainer(unittest.TestCase):
    @mock.patch("subprocess.run")
    def test_encode(self, mock_run):
        # Mock docker build and run calls
        mock_run.side_effect = [
            mock.Mock(returncode=0),  # build
            mock.Mock(
                returncode=0,
                stdout=json.dumps({
                    "quote": "Hello",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "encoded": base64.b64encode(b"Hello").decode()
                }).encode(),
                stderr=b""
            ),
        ]
        # Build image (mocked)
        build_image()
        # Run container (mocked)
        output = run_container("Hello")
        data = json.loads(output)
        self.assertEqual(data["quote"], "Hello")
        self.assertEqual(data["encoded"], base64.b64encode(b"Hello").decode())
        # Verify Docker commands were invoked correctly
        expected_build = mock.call(["docker", "build", "-t", "quote-capsule:latest", "."], check=True)
        expected_run = mock.call(
            ["docker", "run", "-i", "quote-capsule:latest"],
            input=b"Hello",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        mock_run.assert_has_calls([expected_build, expected_run])

    @mock.patch("subprocess.run")
    def test_decode(self, mock_run):
        mock_run.side_effect = [
            mock.Mock(returncode=0),  # build
            mock.Mock(
                returncode=0,
                stdout=json.dumps({"decoded": "World"}).encode(),
                stderr=b""
            ),
        ]
        build_image()
        b64 = base64.b64encode(b"World").decode()
        output = run_container(b64, decode=True)
        data = json.loads(output)
        self.assertEqual(data["decoded"], "World")
        # Verify the --decode flag was passed
        expected_run = mock.call(
            ["docker", "run", "-i", "quote-capsule:latest", "--decode"],
            input=b64.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        mock_run.assert_any_call(expected_run)

if __name__ == "__main__":
    unittest.main()

