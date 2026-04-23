import unittest
import subprocess
import os
import time

# Mock rationale: We are mocking the subprocess.run and docker commands to simulate
# their behavior without actually executing them. This ensures deterministic and offline tests.

class MockCompletedProcess:
    def __init__(self, stdout='', stderr='', returncode=0):
        self.stdout = stdout.encode('utf-8')
        self.stderr = stderr.encode('utf-8')
        self.returncode = returncode

    def __str__(self):
        return f"MockCompletedProcess(returncode={self.returncode})"

class MockSubprocess:
    def __init__(self):
        self.calls = []
        self.mock_results = {}

    def run(self, cmd, capture_output=False, text=False, check=False, **kwargs):
        self.calls.append({'cmd': cmd, 'kwargs': kwargs})
        cmd_tuple = tuple(cmd)
        if cmd_tuple in self.mock_results:
            result = self.mock_results[cmd_tuple]
            if check and result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
            return result
        else:
            # Default behavior for unknown commands
            return MockCompletedProcess(returncode=0)

    def add_mock_result(self, cmd, stdout='', stderr='', returncode=0):
        self.mock_results[tuple(cmd)] = MockCompletedProcess(stdout=stdout, stderr=stderr, returncode=returncode)

    def reset(self):
        self.calls = []
        self.mock_results = {}

class TestDockerEnvManager(unittest.TestCase):

    def setUp(self):
        # Create dummy Dockerfile and entrypoint.sh for testing
        self.test_dir = os.path.join(os.path.dirname(__file__), "..")
        self.entrypoint_path = os.path.join(self.test_dir, "src", "entrypoint.sh")
        self.dummy_dockerfile_content = "FROM alpine:latest\nRUN echo 'hello'"
        self.dummy_dockerfile_path = os.path.join(self.test_dir, "my-test-env.Dockerfile")
        with open(self.dummy_dockerfile_path, "w") as f:
            f.write(self.dummy_dockerfile_content)

        # Mock subprocess.run
        self.mock_subprocess = MockSubprocess()
        self.original_subprocess_run = subprocess.run
        subprocess.run = self.mock_subprocess.run

        # Mock docker socket existence
        self.original_os_path_exists = os.path.exists
        self.original_os_path_is_socket = os.path.is_socket
        os.path.exists = lambda p: True # Assume docker socket path exists
        os.path.is_socket = lambda p: True # Assume it's a socket

    def tearDown(self):
        # Restore original functions
        subprocess.run = self.original_subprocess_run
        os.path.exists = self.original_os_path_exists
        os.path.is_socket = self.original_os_path_is_socket

        # Clean up dummy files
        if os.path.exists(self.dummy_dockerfile_path):
            os.remove(self.dummy_dockerfile_path)
        if os.path.exists(os.path.join(self.test_dir, "Dockerfile")):
            os.remove(os.path.join(self.test_dir, "Dockerfile"))

    def run_entrypoint(self, args):
        command = [self.entrypoint_path] + args
        # We don't need to capture output here as we're checking mock_subprocess.calls
        subprocess.run(command, check=True)

    def test_default_usage(self):
        # Mock the docker commands that will be called
        self.mock_subprocess.add_mock_result(
            ("docker", "build", "-t", "apoc-temp-env-123456789012345678", "-f", self.dummy_dockerfile_path, "."),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "run", "-d", "--name", "my-test-env-env", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "bash"),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "rmi", "apoc-temp-env-123456789012345678"),
            returncode=0
        )

        # Simulate a specific timestamp for predictable container name
        original_date = time.time
        time.time = lambda: 1234567890.12345678

        self.run_entrypoint(["--dockerfile", self.dummy_dockerfile_path])

        time.time = original_date # Restore time function

        # Check if the expected docker commands were called
        self.assertEqual(len(self.mock_subprocess.calls), 3)
        self.assertIn( ("docker", "build", "-t", "apoc-temp-env-123456789012345678", "-f", self.dummy_dockerfile_path, "."), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )
        self.assertIn( ("docker", "run", "-d", "--name", "my-test-env-env", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "bash"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )
        self.assertIn( ("docker", "rmi", "apoc-temp-env-123456789012345678"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )

    def test_custom_command(self):
        self.mock_subprocess.add_mock_result(
            ("docker", "build", "-t", "apoc-temp-env-123456789012345678", "-f", self.dummy_dockerfile_path, "."),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "run", "-d", "--name", "my-test-env-env", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "tail", "-f", "/dev/null"),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "rmi", "apoc-temp-env-123456789012345678"),
            returncode=0
        )

        original_date = time.time
        time.time = lambda: 1234567890.12345678

        self.run_entrypoint(["--dockerfile", self.dummy_dockerfile_path, "--command", "tail -f /dev/null"])

        time.time = original_date

        self.assertEqual(len(self.mock_subprocess.calls), 3)
        self.assertIn( ("docker", "run", "-d", "--name", "my-test-env-env", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "tail", "-f", "/dev/null"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )

    def test_custom_container_name(self):
        self.mock_subprocess.add_mock_result(
            ("docker", "build", "-t", "apoc-temp-env-123456789012345678", "-f", self.dummy_dockerfile_path, "."),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "run", "-d", "--name", "my-custom-container", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "bash"),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "rmi", "apoc-temp-env-123456789012345678"),
            returncode=0
        )

        original_date = time.time
        time.time = lambda: 1234567890.12345678

        self.run_entrypoint(["--dockerfile", self.dummy_dockerfile_path, "--name", "my-custom-container"])

        time.time = original_date

        self.assertEqual(len(self.mock_subprocess.calls), 3)
        self.assertIn( ("docker", "run", "-d", "--name", "my-custom-container", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "bash"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )

    def test_no_docker_socket(self):
        # Mock that docker socket does not exist
        os.path.is_socket = lambda p: False

        self.mock_subprocess.add_mock_result(
            ("docker", "build", "-t", "apoc-temp-env-123456789012345678", "-f", self.dummy_dockerfile_path, "."),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "run", "-d", "--name", "my-test-env-env", "apoc-temp-env-123456789012345678", "bash"),
            returncode=0
        )
        self.mock_subprocess.add_mock_result(
            ("docker", "rmi", "apoc-temp-env-123456789012345678"),
            returncode=0
        )

        original_date = time.time
        time.time = lambda: 1234567890.12345678

        self.run_entrypoint(["--dockerfile", self.dummy_dockerfile_path])

        time.time = original_date

        self.assertEqual(len(self.mock_subprocess.calls), 3)
        # Verify that docker socket is NOT mounted
        self.assertNotIn( ("docker", "run", "-d", "--name", "my-test-env-env", "-v", "/var/run/docker.sock:/var/run/docker.sock", "--privileged", "apoc-temp-env-123456789012345678", "bash"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )
        self.assertIn( ("docker", "run", "-d", "--name", "my-test-env-env", "apoc-temp-env-123456789012345678", "bash"), [tuple(c['cmd']) for c in self.mock_subprocess.calls] )

if __name__ == '__main__':
    unittest.main()
