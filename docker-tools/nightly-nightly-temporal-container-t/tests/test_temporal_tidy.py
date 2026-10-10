import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
import io
import sys

# Mock rationale: We need to test the logic of identifying and reporting
# Docker resources without actually interacting with a live Docker daemon.
# Mocking the docker client and its responses allows for deterministic,
# offline testing of the utility's core functions.

class MockContainer:
    def __init__(self, short_id, name, created_timestamp, status="exited"):
        self.short_id = short_id
        self.name = name
        self.status = status
        self.attrs = {"Created": created_timestamp}
        self.removed = False

    def remove(self):
        self.removed = True

class MockImage:
    def __init__(self, short_id, tags, dangling=False):
        self.short_id = short_id
        self.id = f"sha256:{short_id}" # Full ID for removal
        self.tags = tags
        self.attrs = {"Dangling": dangling} # For filtering, though get_dangling_images uses client.images.list(filters={"dangling": True})

class TestTemporalContainerTidy(unittest.TestCase):

    def setUp(self):
        # Redirect stdout to capture print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('docker.from_env')
    def test_get_stale_containers(self, mock_from_env):
        from temporal_tidy import get_stale_containers

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        now = datetime.now(timezone.utc)
        # Container 1: Stale (older than 24 hours)
        stale_created_ts = (now - timedelta(hours=25)).timestamp()
        mock_container_stale = MockContainer("abc1", "old_app", stale_created_ts)

        # Container 2: Not stale (newer than 24 hours)
        fresh_created_ts = (now - timedelta(hours=10)).timestamp()
        mock_container_fresh = MockContainer("def2", "new_app", fresh_created_ts)

        # Container 3: Running (should not be considered stale by this function)
        running_created_ts = (now - timedelta(hours=30)).timestamp()
        mock_container_running = MockContainer("ghi3", "running_app", running_created_ts, status="running")

        # Mock rationale: The `containers.list` method is mocked to return a predefined
        # set of mock container objects, allowing us to control their properties
        # like creation time and status for testing the `get_stale_containers` logic.
        mock_client.containers.list.return_value = [
            mock_container_stale,
            mock_container_fresh
        ]

        stale = get_stale_containers(mock_client, 24)
        self.assertEqual(len(stale), 1)
        self.assertEqual(stale[0].short_id, "abc1")
        mock_client.containers.list.assert_called_with(all=True, filters={"status": "exited"})

    @patch('docker.from_env')
    def test_get_dangling_images(self, mock_from_env):
        from temporal_tidy import get_dangling_images

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        # Image 1: Dangling
        mock_image_dangling = MockImage("img1", [], dangling=True)
        # Image 2: Not dangling (has tags)
        mock_image_tagged = MockImage("img2", ["myrepo/myimage:latest"], dangling=False)

        # Mock rationale: The `images.list` method is mocked to return a predefined
        # set of mock image objects, allowing us to control their 'dangling' status
        # for testing the `get_dangling_images` logic.
        mock_client.images.list.return_value = [
            mock_image_dangling,
            mock_image_tagged
        ]

        dangling = get_dangling_images(mock_client)
        self.assertEqual(len(dangling), 1)
        self.assertEqual(dangling[0].short_id, "img1")
        mock_client.images.list.assert_called_with(filters={"dangling": True})

    @patch('docker.from_env')
    def test_perform_cleanup_dry_run(self, mock_from_env):
        from temporal_tidy import perform_cleanup

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        now = datetime.now(timezone.utc)
        stale_created_ts = (now - timedelta(hours=25)).timestamp()
        mock_container = MockContainer("abc1", "old_app", stale_created_ts)
        mock_image = MockImage("img1", [], dangling=True)

        perform_cleanup(mock_client, [mock_container], [mock_image], dry_run=True)

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Temporal Defragmentation Dry Run ---", output)
        self.assertIn("Container ID: abc1", output)
        self.assertIn("Image ID: img1", output)
        self.assertFalse(mock_container.removed) # Should not be removed in dry run
        mock_client.images.remove.assert_not_called() # Should not be removed in dry run

    @patch('docker.from_env')
    def test_perform_cleanup_force_clean(self, mock_from_env):
        from temporal_tidy import perform_cleanup

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        now = datetime.now(timezone.utc)
        stale_created_ts = (now - timedelta(hours=25)).timestamp()
        mock_container = MockContainer("abc1", "old_app", stale_created_ts)
        mock_image = MockImage("img1", [], dangling=True)

        # Mock rationale: The `container.remove()` and `client.images.remove()`
        # methods are mocked to verify that they are called when `dry_run` is False.
        # The `MockContainer` also has an internal `removed` flag to confirm its state.
        mock_client.images.remove.return_value = None # Simulate successful removal

        perform_cleanup(mock_client, [mock_container], [mock_image], dry_run=False)

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Initiating Temporal Defragmentation ---", output)
        self.assertIn("Re-aligned container abc1", output)
        self.assertIn("Re-aligned image img1", output)
        self.assertTrue(mock_container.removed) # Should be removed
        mock_client.images.remove.assert_called_once_with(mock_image.id) # Should be removed

    @patch('docker.from_env')
    @patch('sys.argv', ['temporal_tidy.py', '--dry-run'])
    def test_main_dry_run(self, mock_from_env):
        from temporal_tidy import main

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.ping.return_value = True # Mock successful connection

        now = datetime.now(timezone.utc)
        stale_created_ts = (now - timedelta(hours=25)).timestamp()
        mock_container = MockContainer("abc1", "old_app", stale_created_ts)
        mock_image = MockImage("img1", [], dangling=True)

        mock_client.containers.list.return_value = [mock_container]
        mock_client.images.list.return_value = [mock_image]

        # Mock rationale: `sys.argv` is patched to simulate command-line arguments
        # for the `main` function. The `docker.from_env` client and its methods
        # are mocked to control the Docker environment for the test.
        main()

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Temporal Defragmentation Dry Run ---", output)
        self.assertIn("Container ID: abc1", output)
        self.assertIn("Image ID: img1", output)
        self.assertFalse(mock_container.removed)
        mock_client.images.remove.assert_not_called()

    @patch('docker.from_env')
    @patch('sys.argv', ['temporal_tidy.py', '--force-clean'])
    def test_main_force_clean(self, mock_from_env):
        from temporal_tidy import main

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.ping.return_value = True

        now = datetime.now(timezone.utc)
        stale_created_ts = (now - timedelta(hours=25)).timestamp()
        mock_container = MockContainer("abc1", "old_app", stale_created_ts)
        mock_image = MockImage("img1", [], dangling=True)

        mock_client.containers.list.return_value = [mock_container]
        mock_client.images.list.return_value = [mock_image]
        mock_client.images.remove.return_value = None

        main()

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Initiating Temporal Defragmentation ---", output)
        self.assertIn("Re-aligned container abc1", output)
        self.assertIn("Re-aligned image img1", output)
        self.assertTrue(mock_container.removed)
        mock_client.images.remove.assert_called_once_with(mock_image.id)

    @patch('docker.from_env')
    @patch('sys.argv', ['temporal_tidy.py'])
    def test_main_no_args(self, mock_from_env):
        from temporal_tidy import main

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.ping.return_value = True

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Please specify either --dry-run to see what would be removed, or --force-clean to proceed with removal.", output)
        mock_client.containers.list.assert_not_called()
        mock_client.images.list.assert_not_called()

    @patch('docker.from_env', side_effect=Exception("Docker not running"))
    @patch('sys.argv', ['temporal_tidy.py', '--dry-run'])
    def test_main_docker_connection_error(self, mock_from_env):
        from temporal_tidy import main

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("ERROR: Could not connect to Docker daemon. Is Docker running? Docker not running", output)
