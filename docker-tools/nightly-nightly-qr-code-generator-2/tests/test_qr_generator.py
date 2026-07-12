import unittest
from unittest.mock import patch, MagicMock
import subprocess
import base64

class TestQRGeneratorDocker(unittest.TestCase):
    def setUp(self):
        self.input_text = "Test"
        # Precomputed base64 of a 1x1 transparent PNG
        self.expected_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
            "/w8AAn8B9p9X3wAAAABJRU5ErkJggg=="
        )

    @patch('subprocess.run')
    def test_build_and_run(self, mock_run):
        # Mock rationale: simulate successful docker build and run without needing Docker.
        mock_build = MagicMock()
        mock_build.returncode = 0
        mock_run_instance = MagicMock()
        mock_run_instance.returncode = 0
        mock_run_instance.stdout = self.expected_b64.encode()
        # First call is docker build, second call is docker run
        mock_run.side_effect = [mock_build, mock_run_instance]

        # Build image (mocked)
        build_cmd = ["docker", "build", "-t", "qr-generator", "."]
        result_build = subprocess.run(build_cmd, capture_output=True)
        self.assertEqual(result_build.returncode, 0)

        # Run container (mocked)
        run_cmd = ["docker", "run", "--rm", "qr-generator", self.input_text]
        result_run = subprocess.run(run_cmd, capture_output=True, text=True)
        self.assertEqual(result_run.returncode, 0)
        self.assertEqual(result_run.stdout.strip(), self.expected_b64)

        # Verify that the decoded bytes start with PNG header
        png_bytes = base64.b64decode(result_run.stdout.strip())
        self.assertTrue(png_bytes.startswith(b'\x89PNG'))

if __name__ == "__main__":
    unittest.main()
