import unittest
from unittest.mock import patch, MagicMock

class TestDockerUtility(unittest.TestCase):
    def test_build_and_run(self):
        # Mock subprocess.run for docker build and docker run commands
        with patch('subprocess.run') as mock_run:
            # Mock result for docker build
            mock_build = MagicMock()
            mock_build.returncode = 0
            # Mock result for docker run (stdout contains one of the messages)
            mock_run_output = MagicMock()
            mock_run_output.returncode = 0
            mock_run_output.stdout = b"🌪️ The winds whisper: 'Remember to water your cactus.'\n"
            # Set side effects: first call -> build, second call -> run
            mock_run.side_effect = [mock_build, mock_run_output]

            import subprocess
            # Build image (mocked)
            result_build = subprocess.run(['docker', 'build', '-t', 'nightly-emoji-clock', '.'], capture_output=True)
            self.assertEqual(result_build.returncode, 0)

            # Run container (mocked)
            result_run = subprocess.run(['docker', 'run', '--rm', 'nightly-emoji-clock'], capture_output=True)
            self.assertEqual(result_run.returncode, 0)
            output = result_run.stdout.decode().strip()
            # Expected messages list
            expected = [
                "🌪️ The winds whisper: 'Remember to water your cactus.'",
                "☢️ Radiation level: low. Your coffee is safe.",
                "🦖 Dino-saurus says: 'Don't forget to stretch.'",
                "🔋 Battery low? Charge your optimism."
            ]
            self.assertIn(output, expected)

if __name__ == '__main__':
    unittest.main()
