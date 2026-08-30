import unittest
from unittest import mock
import json

class TestDockerSurvivalTipAPI(unittest.TestCase):
    @mock.patch("subprocess.run")
    def test_build_image(self, mock_run):
        # Mock successful docker build
        mock_run.return_value = mock.Mock(returncode=0, stdout=b"", stderr=b"")
        import subprocess
        result = subprocess.run(["docker", "build", "-t", "survival-tip-api", "."], capture_output=True)
        mock_run.assert_called_once()
        self.assertEqual(result.returncode, 0)

    @mock.patch("subprocess.run")
    @mock.patch("urllib.request.urlopen")
    def test_run_container_and_get_tip(self, mock_urlopen, mock_run):
        # Mock docker run (detached)
        mock_run.return_value = mock.Mock(returncode=0, stdout=b"", stderr=b"")
        # Mock HTTP response
        mock_response = mock.Mock()
        mock_response.read.return_value = json.dumps({"tip": "Test tip"}).encode()
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        import subprocess, urllib.request, json
        # Build image (mocked)
        subprocess.run(["docker", "build", "-t", "survival-tip-api", "."], capture_output=True)
        # Run container (mocked)
        subprocess.run(["docker", "run", "--rm", "-p", "8080:8080", "survival-tip-api"], capture_output=True)
        # Query tip (mocked HTTP)
        with urllib.request.urlopen("http://localhost:8080/tip") as resp:
            data = json.loads(resp.read())
        self.assertIn("tip", data)
        self.assertEqual(data["tip"], "Test tip")

if __name__ == "__main__":
    unittest.main()
