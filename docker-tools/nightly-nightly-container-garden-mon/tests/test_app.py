import unittest
from unittest.mock import MagicMock, patch
import json
from src.app import app, get_container_mood, get_container_data

class TestContainerGardenMonitor(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_container_mood_vibrant(self):
        self.assertEqual(get_container_mood("Container is healthy and ready."), {"mood": "Vibrant", "emoji": "🌿", "color": "green"})
        self.assertEqual(get_container_mood("Successfully processed request."), {"mood": "Vibrant", "emoji": "🌿", "color": "green"})

    def test_get_container_mood_wilting(self):
        self.assertEqual(get_container_mood("An error occurred."), {"mood": "Wilting", "emoji": "🥀", "color": "red"})
        self.assertEqual(get_container_mood("Failed to connect to database."), {"mood": "Wilting", "emoji": "🥀", "color": "red"})
        self.assertEqual(get_container_mood("Unhandled exception: IndexError"), {"mood": "Wilting", "emoji": "🥀", "color": "red"})

    def test_get_container_mood_droopy(self):
        self.assertEqual(get_container_mood("Warning: Low disk space."), {"mood": "Droopy", "emoji": "💧", "color": "orange"})
        self.assertEqual(get_container_mood("Request took too long, slow response."), {"mood": "Droopy", "emoji": "💧", "color": "orange"})

    def test_get_container_mood_sprouting(self):
        self.assertEqual(get_container_mood("Starting up service..."), {"mood": "Sprouting", "emoji": "🌱", "color": "lightblue"})
        self.assertEqual(get_container_mood("Initializing components."), {"mood": "Sprouting", "emoji": "🌱", "color": "lightblue"})

    def test_get_container_mood_content(self):
        self.assertEqual(get_container_mood("Just some regular logs."), {"mood": "Content", "emoji": "🌼", "color": "lightgreen"})
        self.assertEqual(get_container_mood(""), {"mood": "Content", "emoji": "🌼", "color": "lightgreen"})

    @patch('src.app.docker.from_env')
    def test_get_container_data(self, mock_docker_from_env):
        # Mock rationale: We don't want to interact with a real Docker daemon during tests.
        # We simulate the Docker client and container objects.

        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client

        # Mock a running container
        mock_container_running = MagicMock()
        mock_container_running.id = "abc123def456"
        mock_container_running.name = "web-app"
        mock_container_running.status = "running"
        mock_container_running.image.tags = ["nginx:latest"]
        mock_container_running.ports = {"80/tcp": [{"HostPort": "8080"}]}
        mock_container_running.logs.return_value = b"Container is healthy and ready.\n" # Mock rationale: Simulate logs for mood detection.

        # Mock an exited container
        mock_container_exited = MagicMock()
        mock_container_exited.id = "xyz789uvw012"
        mock_container_exited.name = "db-service"
        mock_container_exited.status = "exited"
        mock_container_exited.image.tags = ["postgres:13"]
        mock_container_exited.ports = {}
        mock_container_exited.logs.return_value = b"Error: Database connection failed.\n" # Mock rationale: Simulate logs for mood detection.

        # Mock a paused container
        mock_container_paused = MagicMock()
        mock_container_paused.id = "pqr321stu654"
        mock_container_paused.name = "paused-task"
        mock_container_paused.status = "paused"
        mock_container_paused.image.tags = ["ubuntu:latest"]
        mock_container_paused.ports = {}
        mock_container_paused.logs.return_value = b"Task paused.\n" # Mock rationale: Simulate logs for mood detection.

        mock_client.containers.list.return_value = [
            mock_container_running,
            mock_container_exited,
            mock_container_paused
        ]

        data = get_container_data()

        self.assertEqual(len(data), 3)

        # Check running container
        running_container = next(c for c in data if c["name"] == "web-app")
        self.assertEqual(running_container["id"], "abc123def456")
        self.assertEqual(running_container["status"], "running")
        self.assertEqual(running_container["status_emoji"], "🟢")
        self.assertEqual(running_container["mood"], "Vibrant")
        self.assertEqual(running_container["mood_emoji"], "🌿")
        self.assertEqual(running_container["ports"], ["8080->80/tcp"])

        # Check exited container
        exited_container = next(c for c in data if c["name"] == "db-service")
        self.assertEqual(exited_container["id"], "xyz789uvw012")
        self.assertEqual(exited_container["status"], "exited")
        self.assertEqual(exited_container["status_emoji"], "🔴")
        self.assertEqual(exited_container["mood"], "Wilting")
        self.assertEqual(exited_container["mood_emoji"], "🥀")
        self.assertEqual(exited_container["ports"], [])

        # Check paused container
        paused_container = next(c for c in data if c["name"] == "paused-task")
        self.assertEqual(paused_container["id"], "pqr321stu654")
        self.assertEqual(paused_container["status"], "paused")
        self.assertEqual(paused_container["status_emoji"], "⏸️")
        self.assertEqual(paused_container["mood"], "Content") # "Task paused" doesn't trigger specific mood
        self.assertEqual(paused_container["mood_emoji"], "🌼")
        self.assertEqual(paused_container["ports"], [])

    @patch('src.app.docker.from_env')
    def test_api_containers_endpoint(self, mock_docker_from_env):
        # Mock rationale: Similar to test_get_container_data, we mock the Docker client
        # to ensure the API endpoint returns expected data without real Docker interaction.
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client

        mock_container = MagicMock()
        mock_container.id = "test12345678"
        mock_container.name = "test-container"
        mock_container.status = "running"
        mock_container.image.tags = ["test-image:latest"]
        mock_container.ports = {}
        mock_container.logs.return_value = b"Container is healthy.\n"

        mock_client.containers.list.return_value = [mock_container]

        response = self.app.get('/api/containers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "test-container")
        self.assertEqual(data[0]["mood"], "Vibrant")

    @patch('src.app.docker.from_env')
    def test_index_endpoint(self, mock_docker_from_env):
        # Mock rationale: The index endpoint renders HTML, but it calls get_container_data internally.
        # We mock docker.from_env to prevent errors if no Docker daemon is available during test.
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.containers.list.return_value = [] # No containers for simplicity in this test

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Container Garden Monitor", response.data)
        self.assertIn(b"<div id=\"garden\">", response.data)
