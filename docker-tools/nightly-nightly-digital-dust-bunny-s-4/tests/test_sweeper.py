import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dust_bunny_sweeper import prune_resources, calculate_satisfaction, get_docker_client, main

class TestDustBunnySweeper(unittest.TestCase):

    @patch('dust_bunny_sweeper.docker.from_env')
    def test_get_docker_client_success(self, mock_from_env):
        # Mock rationale: Docker client interactions are mocked to ensure tests are deterministic and do not require a running Docker daemon or actual resource manipulation.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.ping.return_value = True

        client = get_docker_client()
        self.assertEqual(client, mock_client)
        mock_from_env.assert_called_once()
        mock_client.ping.assert_called_once()

    @patch('dust_bunny_sweeper.docker.from_env', side_effect=Exception("Docker connection failed"))
    def test_get_docker_client_failure(self, mock_from_env):
        # Mock rationale: Docker client interactions are mocked to ensure tests are deterministic and do not require a running Docker daemon or actual resource manipulation.
        with self.assertRaises(Exception):
            get_docker_client()
        mock_from_env.assert_called_once()

    @patch('dust_bunny_sweeper.docker.from_env')
    def test_prune_resources_no_cleanup(self, mock_from_env):
        # Mock rationale: Docker client interactions are mocked to ensure tests are deterministic and do not require a running Docker daemon or actual resource manipulation.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_client.images.prune.return_value = {'ImagesDeleted': None, 'SpaceReclaimed': 0}
        mock_client.containers.prune.return_value = {'ContainersDeleted': None, 'SpaceReclaimed': 0}
        mock_client.volumes.prune.return_value = {'VolumesDeleted': None, 'SpaceReclaimed': 0}
        mock_client.networks.prune.return_value = {'NetworksDeleted': None}

        cleaned = prune_resources(mock_client)

        self.assertEqual(cleaned, {"images": 0, "containers": 0, "volumes": 0, "networks": 0})
        mock_client.images.prune.assert_called_once_with(filters={'dangling': False})
        mock_client.containers.prune.assert_called_once()
        mock_client.volumes.prune.assert_called_once()
        mock_client.networks.prune.assert_called_once()

    @patch('dust_bunny_sweeper.docker.from_env')
    def test_prune_resources_with_cleanup(self, mock_from_env):
        # Mock rationale: Docker client interactions are mocked to ensure tests are deterministic and do not require a running Docker daemon or actual resource manipulation.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_client.images.prune.return_value = {'ImagesDeleted': ['img1', 'img2'], 'SpaceReclaimed': 100}
        mock_client.containers.prune.return_value = {'ContainersDeleted': ['cont1'], 'SpaceReclaimed': 50}
        mock_client.volumes.prune.return_value = {'VolumesDeleted': ['vol1', 'vol2', 'vol3'], 'SpaceReclaimed': 200}
        mock_client.networks.prune.return_value = {'NetworksDeleted': ['net1']}

        cleaned = prune_resources(mock_client)

        self.assertEqual(cleaned, {"images": 2, "containers": 1, "volumes": 3, "networks": 1})

    @patch('dust_bunny_sweeper.docker.from_env')
    def test_prune_resources_dry_run(self, mock_from_env):
        # Mock rationale: Docker client interactions are mocked to ensure tests are deterministic and do not require a running Docker daemon or actual resource manipulation.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_client.images.prune.return_value = {'ImagesDeleted': ['img1'], 'SpaceReclaimed': 100}
        mock_client.containers.prune.return_value = {'ContainersDeleted': ['cont1'], 'SpaceReclaimed': 50}
        mock_client.volumes.prune.return_value = {'VolumesDeleted': ['vol1'], 'SpaceReclaimed': 200}
        mock_client.networks.prune.return_value = {'NetworksDeleted': ['net1']}

        # Call with dry_run=True
        cleaned = prune_resources(mock_client, dry_run=True)

        # The mock methods should still be called, but the actual Docker client wouldn't perform deletion
        # The return values from the mock are what we assert against for counts
        self.assertEqual(cleaned, {"images": 1, "containers": 1, "volumes": 1, "networks": 1})
        mock_client.images.prune.assert_called_once_with(filters={'dangling': False})
        mock_client.containers.prune.assert_called_once()
        mock_client.volumes.prune.assert_called_once()
        mock_client.networks.prune.assert_called_once()


    def test_calculate_satisfaction(self):
        self.assertEqual(calculate_satisfaction({"images": 0, "containers": 0, "volumes": 0, "networks": 0}), "Content (no dust, but a bit bored)")
        self.assertEqual(calculate_satisfaction({"images": 1, "containers": 0, "volumes": 0, "networks": 0}), "Mildly Pleased (a few tasty crumbs)")
        self.assertEqual(calculate_satisfaction({"images": 4, "containers": 0, "volumes": 0, "networks": 0}), "Mildly Pleased (a few tasty crumbs)")
        self.assertEqual(calculate_satisfaction({"images": 5, "containers": 0, "volumes": 0, "networks": 0}), "Quite Happy (a decent meal!)")
        self.assertEqual(calculate_satisfaction({"images": 19, "containers": 0, "volumes": 0, "networks": 0}), "Quite Happy (a decent meal!)")
        self.assertEqual(calculate_satisfaction({"images": 20, "containers": 0, "volumes": 0, "networks": 0}), "Ecstatic! (a veritable feast of digital dust!)")
        self.assertEqual(calculate_satisfaction({"images": 49, "containers": 0, "volumes": 0, "networks": 0}), "Ecstatic! (a veritable feast of digital dust!)")
        self.assertEqual(calculate_satisfaction({"images": 50, "containers": 0, "volumes": 0, "networks": 0}), "Overjoyed! (a banquet beyond its wildest dreams!)")

    @patch('dust_bunny_sweeper.get_docker_client')
    @patch('dust_bunny_sweeper.prune_resources')
    @patch('dust_bunny_sweeper.calculate_satisfaction')
    @patch('dust_bunny_sweeper.time.sleep')
    @patch.dict(os.environ, {'CLEANUP_INTERVAL_SECONDS': '1', 'DRY_RUN': 'true'})
    def test_main_loop_dry_run(self, mock_sleep, mock_calculate_satisfaction, mock_prune_resources, mock_get_docker_client):
        # Mock rationale: The main loop's external dependencies (Docker client, pruning, sleep) are mocked to control execution flow and prevent actual system changes during testing.
        mock_client = MagicMock()
        mock_get_docker_client.return_value = mock_client
        mock_prune_resources.return_value = {"images": 1, "containers": 0, "volumes": 0, "networks": 0}
        mock_calculate_satisfaction.return_value = "Mildly Pleased"

        # Run main for a short period to test one iteration
        with patch('builtins.exit') as mock_exit: # Prevent actual exit in test
            mock_sleep.side_effect = [None, KeyboardInterrupt] # Exit after one loop
            main()

            mock_get_docker_client.assert_called_once()
            mock_prune_resources.assert_called_once_with(mock_client, dry_run=True)
            mock_calculate_satisfaction.assert_called_once_with({"images": 1, "containers": 0, "volumes": 0, "networks": 0})
            mock_sleep.assert_called_once_with(1)

    @patch('dust_bunny_sweeper.get_docker_client', side_effect=Exception("Client init failed"))
    @patch('dust_bunny_sweeper.logging.error')
    def test_main_client_init_failure(self, mock_logging_error, mock_get_docker_client):
        # Mock rationale: The main loop's external dependencies (Docker client, logging) are mocked to control execution flow and prevent actual system changes during testing.
        with patch('builtins.exit') as mock_exit:
            main()
            mock_get_docker_client.assert_called_once()
            mock_logging_error.assert_called_with("Failed to initialize Docker client. Exiting.")
            # The main function returns, it doesn't call exit() directly in this case.
            # So, mock_exit should not be called.
            mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
