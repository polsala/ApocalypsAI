import unittest
import os
import tempfile
import shutil

# Import the functions from the monitor script
from src.monitor import calculate_file_hash, find_duplicates

class TestEchoChamberMonitor(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def _create_file(self, relative_path, content):
        filepath = os.path.join(self.test_dir, relative_path)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_calculate_file_hash(self):
        # Test hash calculation for a known file content
        filepath = self._create_file('test_file.txt', 'hello world')
        expected_hash = '2c6746ad88d557699742090176184107a731d16181977930774a015383401567'
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

        # Test with empty file
        filepath_empty = self._create_file('empty.txt', '')
        expected_hash_empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        self.assertEqual(calculate_file_hash(filepath_empty), expected_hash_empty)

        # Test with non-existent file
        self.assertIsNone(calculate_file_hash(os.path.join(self.test_dir, 'non_existent.txt')))

    def test_find_duplicates_no_duplicates(self):
        # Mock rationale: Using tempfile.mkdtemp() for actual file system interaction
        # is preferred here to ensure real-world behavior. No external services are involved.
        self._create_file('file1.txt', 'content A')
        self._create_file('file2.txt', 'content B')
        self._create_file('subdir/file3.txt', 'content C')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 0)

    def test_find_duplicates_with_duplicates(self):
        # Mock rationale: Using tempfile.mkdtemp() for actual file system interaction
        # is preferred here to ensure real-world behavior. No external services are involved.
        file_a_path = self._create_file('file_a.txt', 'duplicate content')
        file_b_path = self._create_file('subdir/file_b.txt', 'duplicate content')
        file_c_path = self._create_file('another_file.txt', 'unique content')
        file_d_path = self._create_file('subdir/nested/file_d.txt', 'duplicate content')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)

        # Get the hash of the duplicate content
        duplicate_hash = calculate_file_hash(file_a_path)
        self.assertIn(duplicate_hash, duplicates)

        # Check if all duplicate paths are present
        found_paths = sorted(duplicates[duplicate_hash])
        expected_paths = sorted([file_a_path, file_b_path, file_d_path])
        self.assertEqual(found_paths, expected_paths)

    def test_find_duplicates_multiple_groups(self):
        # Mock rationale: Using tempfile.mkdtemp() for actual file system interaction
        # is preferred here to ensure real-world behavior. No external services are involved.
        file1_path = self._create_file('group1_a.txt', 'content group 1')
        file2_path = self._create_file('group1_b.txt', 'content group 1')
        file3_path = self._create_file('group2_a.txt', 'content group 2')
        file4_path = self._create_file('subdir/group2_b.txt', 'content group 2')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 2)

        hash1 = calculate_file_hash(file1_path)
        hash2 = calculate_file_hash(file3_path)

        self.assertIn(hash1, duplicates)
        self.assertIn(hash2, duplicates)

        self.assertEqual(sorted(duplicates[hash1]), sorted([file1_path, file2_path]))
        self.assertEqual(sorted(duplicates[hash2]), sorted([file3_path, file4_path]))

    def test_find_duplicates_empty_directory(self):
        # Mock rationale: Using tempfile.mkdtemp() for actual file system interaction
        # is preferred here to ensure real-world behavior. No external services are involved.
        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 0)

    def test_find_duplicates_non_existent_directory(self):
        # Mock rationale: No external services are involved. Testing error handling.
        with self.assertRaises(ValueError):
            find_duplicates('/non/existent/path')

    def test_find_duplicates_with_exclusion_patterns(self):
        # Mock rationale: Using tempfile.mkdtemp() for actual file system interaction
        # is preferred here to ensure real-world behavior. No external services are involved.
        self._create_file('file1.txt', 'content A')
        self._create_file('file2.log', 'content A') # Should be excluded by *.log
        self._create_file('temp_dir/file3.txt', 'content A') # Should be excluded by temp_dir/*
        self._create_file('another_dir/file4.txt', 'content A') # Should be included
        self._create_file('another_dir/temp_file.log', 'content A') # Should be excluded by *.log

        # Create a duplicate that should be found
        file_included_1 = self._create_file('included_1.txt', 'duplicate content')
        file_included_2 = self._create_file('subdir/included_2.txt', 'duplicate content')

        # Create a duplicate that should be entirely excluded by directory pattern
        self._create_file('excluded_dir/file_x.txt', 'excluded content')
        self._create_file('excluded_dir/file_y.txt', 'excluded content')
        self._create_file('excluded_dir/nested/file_z.txt', 'excluded content')

        exclude_patterns = ['*.log', 'temp_dir/*', 'excluded_dir/*']
        duplicates = find_duplicates(self.test_dir, exclude_patterns)

        self.assertEqual(len(duplicates), 1)
        duplicate_hash = calculate_file_hash(file_included_1)
        self.assertIn(duplicate_hash, duplicates)
        self.assertEqual(sorted(duplicates[duplicate_hash]), sorted([file_included_1, file_included_2]))

        # Ensure no excluded files or their duplicates are present
        for hash_val, paths in duplicates.items():
            for p in paths:
                self.assertFalse(p.endswith('.log'))
                self.assertFalse('temp_dir' in p)
                self.assertFalse('excluded_dir' in p)

if __name__ == '__main__':
    unittest.main()
