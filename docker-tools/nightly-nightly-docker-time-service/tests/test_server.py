import unittest
import os
import json
from unittest import mock
import importlib.util
from datetime import datetime, timezone

# Dynamically load the server module from src/server.py
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "server.py"))
spec = importlib.util.spec_from_file_location("server", module_path)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

class TestServerLogic(unittest.TestCase):
    def test_get_current_time_with_override(self):
        os.environ["TIME_OVERRIDE"] = "2023-01-01T12:34:56Z"
        self.assertEqual(server.get_current_time(), "2023-01-01T12:34:56Z")
        del os.environ["TIME_OVERRIDE"]

    def test_get_current_time_without_override(self):
        # Mock datetime.utcnow to return a fixed timestamp
        fixed_dt = datetime(2022, 5, 4, 1, 2, 3, tzinfo=timezone.utc)
        with mock.patch('server.datetime') as mock_dt:
            mock_dt.utcnow.return_value = fixed_dt
            mock_dt.fromisoformat.side_effect = datetime.fromisoformat
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(server.get_current_time(), "2022-05-04T01:02:03Z")

    def test_build_response(self):
        os.environ["TIME_OVERRIDE"] = "2023-01-01T00:00:00Z"
        resp = server.build_response()
        self.assertEqual(resp["time"], "2023-01-01T00:00:00Z")
        self.assertEqual(resp["message"], "The stars align in perfect harmony.")
        del os.environ["TIME_OVERRIDE"]

    def test_dockerfile_contains_base_image(self):
        dockerfile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Dockerfile"))
        with open(dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("FROM python:3.11-alpine", content)

if __name__ == "__main__":
    unittest.main()
