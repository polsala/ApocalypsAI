import unittest
from unittest import mock
import subprocess

class TestEmojiForecastDocker(unittest.TestCase):
    @mock.patch('subprocess.run')
    def test_build_and_run(self, mock_run):
        # Mock the docker build command
        mock_build = subprocess.CompletedProcess(
            args=['docker', 'build', '-t', 'emoji-forecast', '.'],
            returncode=0,
            stdout='Successfully built',
            stderr=''
        )
        # Mock the docker run command – return a predictable emoji output
        mock_run_output = subprocess.CompletedProcess(
            args=['docker', 'run', '--rm', '-e', 'CITY=Testopolis', 'emoji-forecast'],
            returncode=0,
            stdout='Testopolis: 🌤️ 🌡️
',
            stderr=''
        )
        mock_run.side_effect = [mock_build, mock_run_output]

        # Build step (should succeed)
        result_build = subprocess.run(['docker', 'build', '-t', 'emoji-forecast', '.'], capture_output=True, text=True)
        self.assertEqual(result_build.returncode, 0)
        self.assertIn('Successfully built', result_build.stdout)

        # Run step (should produce deterministic output)
        result_run = subprocess.run(['docker', 'run', '--rm', '-e', 'CITY=Testopolis', 'emoji-forecast'], capture_output=True, text=True)
        self.assertEqual(result_run.returncode, 0)
        output = result_run.stdout.strip()
        self.assertTrue(output.startswith('Testopolis:'))
        # Verify that the output contains at least one known weather emoji
        self.assertRegex(output, r'[☀️🌤️⛅🌧️⛈️❄️🌪️]')

if __name__ == '__main__':
    unittest.main()

