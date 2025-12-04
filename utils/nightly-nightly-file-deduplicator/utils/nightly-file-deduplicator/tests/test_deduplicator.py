import os
import shutil
import tempfile
import unittest

from deduplicator import find_duplicates, delete_duplicates, move_duplicates


class TestDeduplicator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = self.temp_dir.name
        # File contents
        self.contents = {
            "a.txt": "foo",
            "b.txt": "foo",  # duplicate of a.txt
            "c.txt": "bar",
            "sub/d.txt": "foo",  # duplicate of a.txt in subdir
            "sub/e.txt": "baz",
        }
        for path, text in self.contents.items():
            full_path = os.path.join(self.root, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(text)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_duplicates(self):
        duplicates = find_duplicates(self.root)
        # There should be one hash for "foo" with three files
        self.assertEqual(len(duplicates), 1)
        hash_val, paths = next(iter(duplicates.items()))
        self.assertEqual(len(paths), 3)
        expected_files = {os.path.join(self.root, "a.txt"),
                          os.path.join(self.root, "b.txt"),
                          os.path.join(self.root, "sub/d.txt")}
        self.assertSetEqual(set(paths), expected_files)

    def test_delete_duplicates(self):
        duplicates = find_duplicates(self.root)
        delete_duplicates(duplicates, dry_run=False)
        # After deletion, only one "foo" file should remain
        remaining = [p for p in os.listdir(self.root) if p.endswith(".txt")]
        # a.txt should still exist
        self.assertIn("a.txt", remaining)
        # b.txt and sub/d.txt should be gone
        self.assertNotIn("b.txt", remaining)
        self.assertFalse(os.path.exists(os.path.join(self.root, "sub/d.txt")))

    def test_move_duplicates(self):
        duplicates = find_duplicates(self.root)
        target_dir = os.path.join(self.root, "dup_target")
        move_duplicates(duplicates, target_dir, dry_run=False)
        # After moving, only one "foo" file should remain in original location
        remaining = [p for p in os.listdir(self.root) if p.endswith(".txt")]
        self.assertIn("a.txt", remaining)
        self.assertNotIn("b.txt", remaining)
        # The moved files should be in target_dir
        moved_files = os.listdir(target_dir)
        self.assertIn("b.txt", moved_files)
        self.assertIn("d.txt", moved_files)


if __name__ == "__main__":
    unittest.main()
