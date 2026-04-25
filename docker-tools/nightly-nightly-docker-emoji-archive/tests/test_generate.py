import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from unittest import mock

# Import the generate module from the src directory
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))
import generate

class TestGenerateDockerEmojiArchiver(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to act as the script's location
        self.temp_dir = tempfile.mkdtemp()
        # Copy generate.py into the temp directory
        shutil.copy(src_path / "generate.py", self.temp_dir)
        # Adjust __file__ attribute so generate uses the temp location
        self.original_file = generate.__file__
        generate.__file__ = str(Path(self.temp_dir) / "generate.py")

    def tearDown(self):
        # Restore original __file__ reference
        generate.__file__ = self.original_file
        shutil.rmtree(self.temp_dir)

    @mock.patch('subprocess.run')
    def test_file_creation_and_docker_build_called(self, mock_run):
        # Mock subprocess.run to avoid real Docker invocation
        mock_run.return_value = mock.Mock(returncode=0)
        emojis = ["😀", "🚀"]
        tag = "test-emoji-image"
        # Call main with emojis and tag
        exit_code = generate.main(emojis + [tag])
        self.assertEqual(exit_code, 0)
        # Verify Docker build was invoked with correct arguments
        mock_run.assert_called_once_with(
            ["docker", "build", "-t", tag, "."],
            cwd=mock.ANY,
            check=True
        )
        # Determine the build directory used by the script
        build_dir = Path(generate.__file__).resolve().parent / "build"
        # Check that index.html exists and contains the emojis
        index_path = build_dir / "index.html"
        self.assertTrue(index_path.is_file(), "index.html should be created")
        content = index_path.read_text(encoding="utf-8")
        for e in emojis:
            self.assertIn(e, content)
        # Check that Dockerfile exists and has expected content
        dockerfile_path = build_dir / "Dockerfile"
        self.assertTrue(dockerfile_path.is_file(), "Dockerfile should be created")
        docker_content = dockerfile_path.read_text(encoding="utf-8")
        self.assertIn("FROM nginx:alpine", docker_content)
        self.assertIn("COPY index.html", docker_content)

if __name__ == '__main__':
    unittest.main()
