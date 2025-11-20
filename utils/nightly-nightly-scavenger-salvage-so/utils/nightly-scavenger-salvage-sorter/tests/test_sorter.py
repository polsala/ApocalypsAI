import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from src.sorter import categorize_item, sort_files_in_directory, load_rules, get_file_extension

class TestScavengerSalvageSorter(unittest.TestCase):

    def setUp(self):
        self.rules = load_rules()

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension("document.pdf"), ".pdf")
        self.assertEqual(get_file_extension("archive.tar.gz"), ".gz") # Only last extension
        self.assertEqual(get_file_extension("no_extension"), "")
        self.assertEqual(get_file_extension(".hiddenfile"), "") # No extension after dot
        self.assertEqual(get_file_extension("image.JPG"), ".jpg") # Case insensitive
        self.assertEqual(get_file_extension("folder/file.txt"), ".txt")

    def test_categorize_item_keywords(self):
        self.assertEqual(categorize_item("canned_beans.txt", self.rules), "consumables")
        self.assertEqual(categorize_item("rusty_wrench.log", self.rules), "tools")
        self.assertEqual(categorize_item("broken_radio_parts", self.rules), "electronics")
        self.assertEqual(categorize_item("pile_of_scrap_metal", self.rules), "materials")
        self.assertEqual(categorize_item("old_map_fragment.pdf", self.rules), "documents")
        self.assertEqual(categorize_item("laser_pistol_schematic", self.rules), "weapons")
        self.assertEqual(categorize_item("firstaid_kit_manual", self.rules), "consumables") # 'firstaid' keyword
        self.assertEqual(categorize_item("survival_guide_book", self.rules), "documents") # 'book' keyword

    def test_categorize_item_extensions(self):
        # Test cases where extension might override or be the primary categorizer
        self.assertEqual(categorize_item("important_note.txt", self.rules), "documents")
        self.assertEqual(categorize_item("photo_of_ruins.jpg", self.rules), "misc") # No specific rule, falls to misc
        self.assertEqual(categorize_item("program.py", self.rules), "electronics")
        self.assertEqual(categorize_item("archive.zip", self.rules), "electronics")
        self.assertEqual(categorize_item("schematic.pdf", self.rules), "documents") # 'schematic' keyword takes precedence over '.pdf' extension

    def test_categorize_item_misc(self):
        self.assertEqual(categorize_item("random_rock", self.rules), "misc")
        self.assertEqual(categorize_item("unidentified_object", self.rules), "misc")
        self.assertEqual(categorize_item("strange_artifact.unknown", self.rules), "misc")

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_sort_files_in_directory_dry_run(self, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate file system existence, listing, and file type checks
        # without actually touching the disk. This ensures the test is deterministic and offline.
        mock_exists.side_effect = lambda path: path in ["/mock/source", "/mock/destination"]
        mock_listdir.return_value = ["file1.txt", "tool_kit.bin", "ration_pack.jpg"]
        mock_isfile.return_value = True # All listed items are files

        source_dir = "/mock/source"
        destination_base_dir = "/mock/destination"
        
        results = sort_files_in_directory(source_dir, destination_base_dir, self.rules, dry_run=True)

        self.assertEqual(len(results), 3)
        self.assertIn( (os.path.join(source_dir, "file1.txt"), "documents", os.path.join(destination_base_dir, "documents", "file1.txt")), results)
        self.assertIn( (os.path.join(source_dir, "tool_kit.bin"), "tools", os.path.join(destination_base_dir, "tools", "tool_kit.bin")), results)
        self.assertIn( (os.path.join(source_dir, "ration_pack.jpg"), "consumables", os.path.join(destination_base_dir, "consumables", "ration_pack.jpg")), results)

        mock_makedirs.assert_not_called() # No directories created in dry run
        mock_move.assert_not_called() # No files moved in dry run

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_sort_files_in_directory_actual_run(self, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate file system existence, listing, file type checks,
        # directory creation, and file movement without actual disk I/O. This ensures
        # the test is deterministic and offline.
        
        # Simulate initial state: source exists, destination does not initially.
        # We'll track created paths to make mock_exists behave dynamically.
        existing_paths = {"/mock/source"}
        def custom_exists(path):
            return path in existing_paths
        mock_exists.side_effect = custom_exists

        def custom_makedirs(path, exist_ok=False):
            if not exist_ok and path in existing_paths:
                # In a real scenario, os.makedirs might raise FileExistsError if exist_ok is False
                # but for this mock, we just ensure it's added to existing_paths.
                pass 
            existing_paths.add(path)
        mock_makedirs.side_effect = custom_makedirs

        mock_listdir.return_value = ["file1.txt", "tool_kit.bin", "ration_pack.jpg"]
        mock_isfile.return_value = True

        source_dir = "/mock/source"
        destination_base_dir = "/mock/destination"
        
        results = sort_files_in_directory(source_dir, destination_base_dir, self.rules, dry_run=False)

        self.assertEqual(len(results), 3)
        self.assertIn( (os.path.join(source_dir, "file1.txt"), "documents", os.path.join(destination_base_dir, "documents", "file1.txt")), results)
        self.assertIn( (os.path.join(source_dir, "tool_kit.bin"), "tools", os.path.join(destination_base_dir, "tools", "tool_kit.bin")), results)
        self.assertIn( (os.path.join(source_dir, "ration_pack.jpg"), "consumables", os.path.join(destination_base_dir, "consumables", "ration_pack.jpg")), results)

        # Check that destination base dir was created
        mock_makedirs.assert_any_call(destination_base_dir)
        # Check that category directories were created
        mock_makedirs.assert_any_call(os.path.join(destination_base_dir, "documents"))
        mock_makedirs.assert_any_call(os.path.join(destination_base_dir, "tools"))
        mock_makedirs.assert_any_call(os.path.join(destination_base_dir, "consumables"))
        
        # Check that files were moved
        mock_move.assert_any_call(os.path.join(source_dir, "file1.txt"), os.path.join(destination_base_dir, "documents", "file1.txt"))
        mock_move.assert_any_call(os.path.join(source_dir, "tool_kit.bin"), os.path.join(destination_base_dir, "tools", "tool_kit.bin"))
        mock_move.assert_any_call(os.path.join(source_dir, "ration_pack.jpg"), os.path.join(destination_base_dir, "consumables", "ration_pack.jpg"))
        self.assertEqual(mock_move.call_count, 3)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_sort_files_in_directory_source_not_exists(self, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate the scenario where the source directory does not exist.
        # This ensures the utility handles invalid input gracefully without errors.
        mock_exists.return_value = False # Source directory does not exist
        
        source_dir = "/nonexistent/source"
        destination_base_dir = "/mock/destination"
        
        results = sort_files_in_directory(source_dir, destination_base_dir, self.rules)
        
        self.assertEqual(results, [])
        mock_listdir.assert_not_called() # Should not try to list files
        mock_isfile.assert_not_called() # Should not try to check file types

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_sort_files_in_directory_move_error(self, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate a file system error during the move operation (e.g., permissions).
        # This ensures the utility logs the error and continues processing other files if any.
        existing_paths = {"/mock/source"}
        def custom_exists(path):
            return path in existing_paths
        mock_exists.side_effect = custom_exists

        def custom_makedirs(path, exist_ok=False):
            if not exist_ok and path in existing_paths:
                pass 
            existing_paths.add(path)
        mock_makedirs.side_effect = custom_makedirs

        mock_listdir.return_value = ["problem_file.txt"]
        mock_isfile.return_value = True
        mock_move.side_effect = Exception("Permission denied") # Simulate an error during move

        source_dir = "/mock/source"
        destination_base_dir = "/mock/destination"
        
        results = sort_files_in_directory(source_dir, destination_base_dir, self.rules, dry_run=False)
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0][0] == os.path.join(source_dir, "problem_file.txt"))
        self.assertTrue(results[0][1] == "documents")
        self.assertIn("ERROR: Permission denied", results[0][2]) # Check for error message in result

        mock_move.assert_called_once_with(os.path.join(source_dir, "problem_file.txt"), os.path.join(destination_base_dir, "documents", "problem_file.txt"))


if __name__ == '__main__':
    unittest.main()
