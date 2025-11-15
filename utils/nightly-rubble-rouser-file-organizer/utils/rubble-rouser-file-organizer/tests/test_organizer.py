import unittest
import os
import shutil
import tempfile
from unittest.mock import patch

# Mock rationale: We are testing the file organization logic, not the actual file system operations
# in a live environment. Using a temporary directory ensures tests are isolated, deterministic,
# and do not affect the user's file system. We don't need to mock os.path.exists, os.makedirs,
# shutil.move, etc., because tempfile provides a real, isolated file system context.

# Import the function to be tested
import sys
# Add the src directory to the Python path to allow importing organizer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from organizer import organize_directory, FILE_CATEGORIES

class TestRubbleRouserFileOrganizer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        os.makedirs(self.source_dir)

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    def _create_file(self, filename, content="dummy content"):
        filepath = os.path.join(self.source_dir, filename)
        # Ensure parent directories exist if filename includes paths
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_empty_directory(self, mock_print):
        organize_directory(self.source_dir)
        # Only category directories should exist, no files moved
        self.assertEqual(len(os.listdir(self.source_dir)), len(FILE_CATEGORIES))
        for category in FILE_CATEGORIES:
            self.assertTrue(os.path.isdir(os.path.join(self.source_dir, category)))

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_various_file_types(self, mock_print):
        self._create_file("document.pdf")
        self._create_file("image.jpg")
        self._create_file("video.mp4")
        self._create_file("archive.zip")
        self._create_file("script.py")
        self._create_file("unknown.xyz")
        self._create_file("audio.mp3")

        organize_directory(self.source_dir)

        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Documents", "document.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Images", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Videos", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Archives", "archive.zip")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Code", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Others", "unknown.xyz")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Audio", "audio.mp3")))

        # Check that original files are gone from the source_dir root (excluding category dirs)
        remaining_items = [f for f in os.listdir(self.source_dir) if os.path.isfile(os.path.join(self.source_dir, f))]
        self.assertEqual(len(remaining_items), 0)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_directory_with_subdirectories(self, mock_print):
        self._create_file("document.pdf")
        subdir_path = os.path.join(self.source_dir, "subdir")
        os.makedirs(subdir_path)
        self._create_file("subdir/nested.txt") # This file should not be moved by the current logic

        organize_directory(self.source_dir)

        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Documents", "document.pdf")))
        self.assertTrue(os.path.isdir(subdir_path))
        self.assertTrue(os.path.exists(os.path.join(subdir_path, "nested.txt")))
        
        # Ensure the nested file was not moved to 'Others' or any other category
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "Others", "nested.txt")))

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_file_already_in_correct_category(self, mock_print):
        # Create the category directory first
        doc_dir = os.path.join(self.source_dir, "Documents")
        os.makedirs(doc_dir)
        self._create_file("Documents/existing_doc.pdf") # Create it directly in the target

        organize_directory(self.source_dir)

        # It should still be there and not moved/duplicated
        self.assertTrue(os.path.exists(os.path.join(doc_dir, "existing_doc.pdf")))
        # Check that the print statement for skipping was called
        mock_print.assert_any_call(f"[Rubble-Rouser] Relic 'existing_doc.pdf' already in its designated 'Zone Documents'. Skipping.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_duplicate_file_name_in_target(self, mock_print):
        # Create a file in the source
        self._create_file("report.pdf", content="source content")
        # Create a file with the same name in the target category directory
        doc_dir = os.path.join(self.source_dir, "Documents")
        os.makedirs(doc_dir)
        self._create_file("Documents/report.pdf", content="original content")

        organize_directory(self.source_dir)

        # The file from source should NOT overwrite the existing one
        self.assertTrue(os.path.exists(os.path.join(doc_dir, "report.pdf")))
        with open(os.path.join(doc_dir, "report.pdf"), 'r') as f:
            self.assertEqual(f.read(), "original content") # Ensure content is not overwritten
        
        # The original file in source_dir should remain untouched
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "report.pdf")))
        with open(os.path.join(self.source_dir, "report.pdf"), 'r') as f:
            self.assertEqual(f.read(), "source content") # Ensure content is not moved
        mock_print.assert_any_call(f"[Rubble-Rouser] WARNING: Duplicate relic 'report.pdf' found in 'Zone Documents'. Skipping to prevent overwrite.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_non_existent_directory(self, mock_print):
        non_existent_dir = os.path.join(self.test_dir, "non_existent")
        organize_directory(non_existent_dir)
        mock_print.assert_any_call(f"[Rubble-Rouser] ERROR: Source directory '{non_existent_dir}' not found. Aborting salvage operation.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_directory_with_only_category_dirs(self, mock_print):
        # Create all category directories, but no files outside them
        for category in FILE_CATEGORIES:
            os.makedirs(os.path.join(self.source_dir, category), exist_ok=True)
        
        organize_directory(self.source_dir)
        
        # No files should be moved, only category directories should exist
        self.assertEqual(len(os.listdir(self.source_dir)), len(FILE_CATEGORIES))
        for category in FILE_CATEGORIES:
            self.assertTrue(os.path.isdir(os.path.join(self.source_dir, category)))

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output
    def test_organize_file_with_no_extension(self, mock_print):
        self._create_file("noextensionfile")
        organize_directory(self.source_dir)
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "Others", "noextensionfile")))

if __name__ == '__main__':
    unittest.main()
