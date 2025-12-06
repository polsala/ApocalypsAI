import unittest
import os
import shutil
import tempfile
import hashlib
from unittest.mock import patch, mock_open

# Import the functions to be tested
from src.organizer import get_file_category, calculate_file_hash, organize_stash, find_duplicates, CATEGORIES

class TestScavengerStashOrganizer(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for testing
        self.test_source_dir = tempfile.mkdtemp()
        self.test_dest_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_source_dir)
        self.addCleanup(shutil.rmtree, self.test_dest_dir)

    def _create_dummy_file(self, directory, filename, content="dummy content"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_get_file_category(self):
        self.assertEqual(get_file_category('report.pdf'), 'documents')
        self.assertEqual(get_file_category('photo.JPG'), 'images')
        self.assertEqual(get_file_category('song.flac'), 'audio')
        self.assertEqual(get_file_category('movie.mkv'), 'videos')
        self.assertEqual(get_file_category('archive.zip'), 'archives')
        self.assertEqual(get_file_category('script.sh'), 'executables')
        self.assertEqual(get_file_category('unknown.xyz'), 'others')
        self.assertEqual(get_file_category('no_extension'), 'others')

    def test_calculate_file_hash(self):
        # Mock rationale: We don't want to hit the actual filesystem for hash calculation
        # in a unit test. We mock `open` to control file content.
        mock_file_content = b'test data for hashing'
        expected_hash = hashlib.md5(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            # The actual filepath doesn't matter here, as open is mocked
            calculated_hash = calculate_file_hash('/fake/path/to/file.txt')
            self.assertEqual(calculated_hash, expected_hash)
            m_open.assert_called_once_with('/fake/path/to/file.txt', 'rb')

    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests
    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Simplify path comparisons for testing
    def test_organize_stash(self, mock_abspath, mock_print, mock_os_walk, mock_os_path_exists, mock_makedirs, mock_shutil_move):
        # Mock rationale: We don't want to perform actual file system moves or creations.
        # We simulate the directory structure and file movements.

        # Simulate source directory content
        mock_os_walk.return_value = [
            (self.test_source_dir, [], ['doc1.pdf', 'image1.jpg']),
            (os.path.join(self.test_source_dir, 'subfolder'), [], ['video1.mp4', 'other.log'])
        ]

        organize_stash(self.test_source_dir, self.test_dest_dir)

        # Assert category directories were created
        mock_makedirs.assert_any_call(os.path.join(self.test_dest_dir, 'documents'), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(self.test_dest_dir, 'images'), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(self.test_dest_dir, 'videos'), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(self.test_dest_dir, 'others'), exist_ok=True)

        # Assert files were moved to correct categories
        mock_shutil_move.assert_any_call(
            os.path.join(self.test_source_dir, 'doc1.pdf'), 
            os.path.join(self.test_dest_dir, 'documents', 'doc1.pdf')
        )
        mock_shutil_move.assert_any_call(
            os.path.join(self.test_source_dir, 'image1.jpg'), 
            os.path.join(self.test_dest_dir, 'images', 'image1.jpg')
        )
        mock_shutil_move.assert_any_call(
            os.path.join(self.test_source_dir, 'subfolder', 'video1.mp4'), 
            os.path.join(self.test_dest_dir, 'videos', 'video1.mp4')
        )
        mock_shutil_move.assert_any_call(
            os.path.join(self.test_source_dir, 'subfolder', 'other.log'), 
            os.path.join(self.test_dest_dir, 'others', 'other.log')
        )
        self.assertEqual(mock_shutil_move.call_count, 4)

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('src.organizer.calculate_file_hash') # Mock rationale: Avoid actual file hashing for speed and determinism.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests
    def test_find_duplicates(self, mock_print, mock_calculate_file_hash, mock_os_walk, mock_os_path_exists):
        # Simulate directory content with duplicates
        mock_os_walk.return_value = [
            (self.test_dest_dir, [], ['fileA.txt', 'fileB.txt']),
            (os.path.join(self.test_dest_dir, 'sub'), [], ['fileC.txt'])
        ]

        # Assign hashes such that fileB and fileC are duplicates
        mock_calculate_file_hash.side_effect = [
            'hash_unique_A',  # for fileA.txt
            'hash_duplicate', # for fileB.txt
            'hash_duplicate'  # for fileC.txt (duplicate of fileB)
        ]

        duplicates = find_duplicates(self.test_dest_dir)

        expected_duplicates = {
            'hash_duplicate': [
                os.path.join(self.test_dest_dir, 'fileB.txt'),
                os.path.join(self.test_dest_dir, 'sub', 'fileC.txt')
            ]
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(mock_calculate_file_hash.call_count, 3)

    @patch('src.organizer.organize_stash')
    @patch('src.organizer.find_duplicates')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main(self, mock_parse_args, mock_find_duplicates, mock_organize_stash):
        # Mock rationale: Test the main function's orchestration without running
        # the full file system operations. We ensure it calls the sub-functions correctly.
        
        # Simulate command-line arguments
        mock_parse_args.return_value.source_directory = self.test_source_dir
        mock_parse_args.return_value.destination_directory = self.test_dest_dir

        from src.organizer import main # Import main after patching to ensure patches apply
        main()

        mock_organize_stash.assert_called_once_with(self.test_source_dir, self.test_dest_dir)
        mock_find_duplicates.assert_called_once_with(self.test_dest_dir)

if __name__ == '__main__':
    unittest.main()
