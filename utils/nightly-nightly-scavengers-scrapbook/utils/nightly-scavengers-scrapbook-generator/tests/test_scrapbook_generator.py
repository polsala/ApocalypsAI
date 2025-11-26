import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing scrapbook_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scrapbook_generator import generate_scrapbook
sys.path.pop(0)

class TestScrapbookGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: os.path.join is a pure function, but mocking it to pass through allows us to control its behavior if needed, while still using real path joining for simplicity here.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: We need to simulate file reading and writing without touching the actual filesystem.
    def test_generate_scrapbook_success(self, mock_open_func, mock_os_path_join, mock_os_path_isfile, mock_os_listdir, mock_os_path_isdir):
        # Mock rationale: Simulate the existence of the input directory.
        mock_os_path_isdir.return_value = True

        # Mock rationale: Simulate files in the input directory. Sorted alphabetically for deterministic testing.
        mock_os_listdir.return_value = ['note_a.txt', 'image.jpg', 'note_b.txt']

        # Mock rationale: Indicate which items from os.listdir are actual files.
        mock_os_path_isfile.side_effect = lambda x: x.endswith('.txt') or x.endswith('.jpg')

        # Mock rationale: Simulate the content of the .txt files.
        mock_file_contents = {
            'input_dir/note_a.txt': 'Content of note A.',
            'input_dir/note_b.txt': 'Content of note B.'
        }

        # Configure mock_open for reading files
        def mock_open_side_effect(file_path, mode='r', encoding=None):
            if mode == 'r':
                # Mock rationale: Return a mock file handle with specific content when reading.
                mock_file = mock_open_func.return_value
                mock_file.read.return_value = mock_file_contents.get(file_path, '')
                return mock_file
            elif mode == 'w':
                # Mock rationale: Return a mock file handle for writing, capturing the written data.
                return mock_open_func.return_value
            raise ValueError(f"Unexpected mode: {mode}")

        mock_open_func.side_effect = mock_open_side_effect

        input_dir = 'input_dir'
        output_file = 'output.txt'

        generate_scrapbook(input_dir, output_file)

        # Assertions for output file writing
        # Mock rationale: Check that the output file was opened for writing.
        mock_open_func.assert_any_call(output_file, 'w', encoding='utf-8')

        # Mock rationale: Verify the content written to the output file.
        expected_output = (
            "--- Entry from note_a.txt ---\n"
            "Content of note A.\n\n"
            "--- Entry from note_b.txt ---\n"
            "Content of note B.\n\n"
        )
        mock_open_func.return_value.write.assert_called_once_with(expected_output)

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_scrapbook_empty_dir(self, mock_open_func, mock_os_path_join, mock_os_path_isfile, mock_os_listdir, mock_os_path_isdir):
        # Mock rationale: Simulate the existence of the input directory.
        mock_os_path_isdir.return_value = True
        # Mock rationale: Simulate an empty directory.
        mock_os_listdir.return_value = []
        mock_os_path_isfile.return_value = False

        input_dir = 'empty_dir'
        output_file = 'output.txt'

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            generate_scrapbook(input_dir, output_file)
            self.assertIn("No .txt files found", mock_stdout.getvalue())

        # Mock rationale: Ensure no file was opened for writing if no content.
        mock_open_func.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_scrapbook_non_existent_dir(self, mock_open_func, mock_os_path_join, mock_os_path_isfile, mock_os_listdir, mock_os_path_isdir):
        # Mock rationale: Simulate a non-existent input directory.
        mock_os_path_isdir.return_value = False

        input_dir = 'non_existent_dir'
        output_file = 'output.txt'

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            generate_scrapbook(input_dir, output_file)
            self.assertIn("Error: Input directory 'non_existent_dir' not found.", mock_stdout.getvalue())

        # Mock rationale: Ensure no file was opened for writing.
        mock_open_func.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_scrapbook_file_read_error(self, mock_open_func, mock_os_path_join, mock_os_path_isfile, mock_os_listdir, mock_os_path_isdir):
        # Mock rationale: Simulate the existence of the input directory.
        mock_os_path_isdir.return_value = True
        # Mock rationale: Simulate a single .txt file.
        mock_os_listdir.return_value = ['corrupt_note.txt']
        mock_os_path_isfile.return_value = True

        # Configure mock_open to raise an IOError when reading the specific file
        def mock_open_side_effect(file_path, mode='r', encoding=None):
            if mode == 'r' and 'corrupt_note.txt' in file_path:
                # Mock rationale: Simulate an IOError during file reading.
                raise IOError("Permission denied")
            elif mode == 'w':
                # Mock rationale: Allow writing to the output file.
                return mock_open_func.return_value
            raise ValueError(f"Unexpected mode: {mode}")

        mock_open_func.side_effect = mock_open_side_effect

        input_dir = 'input_dir'
        output_file = 'output.txt'

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            generate_scrapbook(input_dir, output_file)
            self.assertIn("Warning: Could not read file 'corrupt_note.txt': Permission denied", mock_stdout.getvalue())

        # Mock rationale: Check that the output file was opened and the error message was written.
        mock_open_func.assert_any_call(output_file, 'w', encoding='utf-8')
        expected_output = (
            "--- Entry from corrupt_note.txt ---\n"
            "[Error reading file: Permission denied]\n\n"
        )
        mock_open_func.return_value.write.assert_called_once_with(expected_output)

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.listdir')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_scrapbook_output_write_error(self, mock_open_func, mock_os_path_join, mock_os_listdir, mock_os_path_isfile, mock_os_path_isdir):
        # Mock rationale: Simulate the existence of the input directory.
        mock_os_path_isdir.return_value = True
        # Mock rationale: Simulate a single .txt file.
        mock_os_listdir.return_value = ['note.txt']
        mock_os_path_isfile.return_value = True

        # Mock rationale: Simulate content for the input file.
        mock_file_contents = {
            'input_dir/note.txt': 'Some content.'
        }

        # Configure mock_open to raise an IOError when opening the output file for writing
        def mock_open_side_effect(file_path, mode='r', encoding=None):
            if mode == 'r':
                mock_file = mock_open_func.return_value
                mock_file.read.return_value = mock_file_contents.get(file_path, '')
                return mock_file
            elif mode == 'w':
                # Mock rationale: Simulate an IOError when trying to open the output file for writing.
                raise IOError("Disk full")
            raise ValueError(f"Unexpected mode: {mode}")

        mock_open_func.side_effect = mock_open_side_effect

        input_dir = 'input_dir'
        output_file = 'output.txt'

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            generate_scrapbook(input_dir, output_file)
            self.assertIn("Error writing to output file 'output.txt': Disk full", mock_stdout.getvalue())

        # Mock rationale: Verify that the output file was attempted to be opened for writing.
        mock_open_func.assert_any_call(output_file, 'w', encoding='utf-8')
        # Mock rationale: Ensure no content was written if the file couldn't be opened.
        mock_open_func.return_value.write.assert_not_called()
