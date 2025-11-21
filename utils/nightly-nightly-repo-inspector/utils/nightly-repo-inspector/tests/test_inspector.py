import json
import os
import tempfile
import unittest
from pathlib import Path

# Mock rationale: using temporary files ensures deterministic environment without external I/O.

from src.inspector import inspect_path


class TestRepoInspector(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary directory with a known structure
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        # Create files of various extensions and sizes
        (base / "a.py").write_bytes(b"print('hello')")  # 15 bytes
        (base / "b.txt").write_bytes(b"sample text")      # 11 bytes
        (base / "c.md").write_bytes(b"# Title\n\nContent")  # 18 bytes
        # Nested directory
        nested = base / "nested"
        nested.mkdir()
        (nested / "d.py").write_bytes(b"def foo():\n    pass")  # 20 bytes
        (nested / "e").write_bytes(b"no extension")          # 12 bytes

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_inspect_path(self):
        result = inspect_path(Path(self.temp_dir.name))
        # Expected counts and sizes
        expected = {
            "total_files": 5,
            "total_size": 15 + 11 + 18 + 20 + 12,
            "extensions": {
                ".py": {"count": 2, "size": 15 + 20},
                ".txt": {"count": 1, "size": 11},
                ".md": {"count": 1, "size": 18},
                "<no-ext>": {"count": 1, "size": 12},
            },
        }
        # Convert both to JSON strings for easy deep comparison (order of keys may differ)
        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(expected, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
