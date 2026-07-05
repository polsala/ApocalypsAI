import unittest
from pathlib import Path\n\nclass TestDockerfile(unittest.TestCase):
    def setUp(self):
        self.dockerfile_path = Path(__file__).parents[1] / "src" / "Dockerfile"\n        self.content = self.dockerfile_path.read_text()\n\n    def test_base_image(self):
        # Mock rationale: ensure the image uses a lightweight Python base
        self.assertIn("FROM python:3.11-slim", self.content)\n\n    def test_workdir(self):
        self.assertIn("WORKDIR /app", self.content)\n\n    def test_expose_port(self):
        self.assertIn("EXPOSE 8080", self.content)\n\n    def test_cmd(self):
        # Mock rationale: verify the container starts the Flask app correctly
        self.assertIn('CMD ["python","app.py"]', self.content)\n\nif __name__ == "__main__":
    unittest.main()\n
