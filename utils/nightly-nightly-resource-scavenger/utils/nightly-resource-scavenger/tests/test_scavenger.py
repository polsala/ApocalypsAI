import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
from src.scavenger import scavenge_resources, is_text_file

class TestScavenger(unittest.TestCase):

    @patch('os.path.abspath', return_value='/mock/path')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.scavenger.is_text_file') # Mock our own heuristic
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_no_matching_files(self, mock_file_open, mock_is_text_file, mock_getsize, mock_os_walk, mock_abspath):
        # Mock rationale: os.walk is a file system traversal function, needs to be mocked for deterministic, offline tests.
        # Mock rationale: os.path.getsize interacts with the file system.
        # Mock rationale: is_text_file is a file system interaction heuristic.
        # Mock rationale: builtins.open is for file I/O, essential to mock for offline tests.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file1.jpg', 'file2.png'])
        ]
        mock_is_text_file.return_value = False # No files are text files for this test
        mock_getsize.return_value = 100

        result = scavenge_resources('/mock/dir', ['.txt', '.md'], 'report.txt')

        self.assertTrue(result)
        mock_file_open.assert_called_once_with('report.txt', 'w', encoding='utf-8')
        handle = mock_file_open()
        report_content = handle.write.call_args[0][0]
        self.assertIn("Total files found matching criteria: 0", report_content)
        self.assertNotIn("### Found Resource:", report_content)

    @patch('os.path.abspath', return_value='/mock/path')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.scavenger.is_text_file')
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_with_matching_text_files(self, mock_file_open, mock_is_text_file, mock_getsize, mock_os_walk, mock_abspath):
        # Mock rationale: Same as above, simulating file system interactions.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['doc.txt', 'image.png', 'notes.md']),
            ('/mock/dir/subdir', [], ['report.log'])
        ]
        mock_is_text_file.side_effect = lambda f: f.endswith(('.txt', '.md', '.log')) # Simulate text files
        mock_getsize.return_value = 123 # Arbitrary size

        # Create a dictionary of file contents
        file_contents = {
            '/mock/dir/doc.txt': "Line 1 of doc.txt\nLine 2 of doc.txt\nLine 3\nLine 4\nLine 5\nLine 6",
            '/mock/dir/notes.md': "# My Notes\n- Item 1\n- Item 2",
            '/mock/dir/subdir/report.log': "Error: Something happened\nInfo: All good"
        }

        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'w' in mode: # This is the report file
                return mock_file_open.return_value # Return the mock_open's default handle for writing
            else: # This is for reading source files
                mock_file_handle = MagicMock()
                mock_file_handle.__enter__.return_value = mock_file_handle
                mock_file_handle.__exit__.return_value = None
                mock_file_handle.__iter__.return_value = iter(file_contents.get(filepath, "").splitlines())
                mock_file_handle.read.return_value = file_contents.get(filepath, "")
                return mock_file_handle

        mock_file_open.side_effect = mock_open_side_effect

        result = scavenge_resources('/mock/dir', ['.txt', '.md', '.log'], 'report.txt', max_content_lines=3)

        self.assertTrue(result)
        # Check that the report file was opened for writing
        mock_file_open.assert_any_call('report.txt', 'w', encoding='utf-8')
        
        # Get the content written to the report
        report_content = ""
        for call_args in mock_file_open.return_value.write.call_args_list:
            report_content += call_args[0][0]

        self.assertIn("Total files found matching criteria: 3", report_content)
        self.assertIn("### Found Resource: /mock/dir/doc.txt", report_content)
        self.assertIn("Line 1 of doc.txt", report_content)
        self.assertIn("... (truncated after 3 lines)", report_content)
        self.assertIn("### Found Resource: /mock/dir/notes.md", report_content)
        self.assertIn("# My Notes", report_content)
        self.assertIn("### Found Resource: /mock/dir/subdir/report.log", report_content)
        self.assertIn("Error: Something happened", report_content)

    @patch('os.path.abspath', return_value='/mock/path')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.scavenger.is_text_file')
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_with_binary_file(self, mock_file_open, mock_is_text_file, mock_getsize, mock_os_walk, mock_abspath):
        # Mock rationale: Simulating a scenario with a binary file.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['binary.bin', 'text.txt'])
        ]
        mock_is_text_file.side_effect = lambda f: f.endswith('.txt') # Only text.txt is text
        mock_getsize.return_value = 500

        file_contents = {
            '/mock/dir/text.txt': "This is a text file."
        }
        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'w' in mode:
                return mock_file_open.return_value
            else:
                mock_file_handle = MagicMock()
                mock_file_handle.__enter__.return_value = mock_file_handle
                mock_file_handle.__exit__.return_value = None
                mock_file_handle.__iter__.return_value = iter(file_contents.get(filepath, "").splitlines())
                mock_file_handle.read.return_value = file_contents.get(filepath, "")
                return mock_file_handle
        mock_file_open.side_effect = mock_open_side_effect

        result = scavenge_resources('/mock/dir', ['.bin', '.txt'], 'report.txt')

        self.assertTrue(result)
        report_content = ""
        for call_args in mock_file_open.return_value.write.call_args_list:
            report_content += call_args[0][0]

        self.assertIn("### Found Resource: /mock/dir/binary.bin", report_content)
        self.assertIn("Content: [Binary or non-text file - content skipped]", report_content)
        self.assertIn("### Found Resource: /mock/dir/text.txt", report_content)
        self.assertIn("This is a text file.", report_content)
        self.assertIn("Total files found matching criteria: 2", report_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_is_text_file_true(self, mock_file_open):
        # Mock rationale: Testing the internal heuristic for text files.
        mock_file_open.return_value.__enter__.return_value.read.return_value = "Hello, world!"
        self.assertTrue(is_text_file("dummy.txt"))

    @patch('builtins.open', new_callable=mock_open)
    def test_is_text_file_false_on_decode_error(self, mock_file_open):
        # Mock rationale: Simulating a UnicodeDecodeError for a binary file.
        mock_file_open.return_value.__enter__.return_value.read.side_effect = UnicodeDecodeError('utf-8', b'\x80', 0, 1, 'invalid byte')
        self.assertFalse(is_text_file("dummy.bin"))

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_is_text_file_false_on_io_error(self, mock_file_open):
        # Mock rationale: Simulating an IOError (e.g., permission denied) for a file.
        self.assertFalse(is_text_file("protected.txt"))

    @patch('os.path.abspath', return_value='/mock/path')
    @patch('os.walk', side_effect=OSError("Cannot access directory"))
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_directory_access_error(self, mock_file_open, mock_os_walk, mock_abspath):
        # Mock rationale: Simulating an error during directory traversal.
        result = scavenge_resources('/mock/dir', ['.txt'], 'report.txt')
        self.assertFalse(result)
        # Ensure no report was written or it contains an error message
        mock_file_open.assert_not_called() # No report file should be opened for writing if os.walk fails early.

    @patch('os.path.abspath', return_value='/mock/path')
    @patch('os.walk')
    @patch('os.path.getsize', side_effect=OSError("File not found"))
    @patch('src.scavenger.is_text_file')
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_file_size_error(self, mock_file_open, mock_is_text_file, mock_getsize, mock_os_walk, mock_abspath):
        # Mock rationale: Simulating an error when getting file size.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file.txt'])
        ]
        mock_is_text_file.return_value = True
        
        file_contents = {
            '/mock/dir/file.txt': "Content"
        }
        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'w' in mode:
                return mock_file_open.return_value
            else:
                mock_file_handle = MagicMock()
                mock_file_handle.__enter__.return_value = mock_file_handle
                mock_file_handle.__exit__.return_value = None
                mock_file_handle.__iter__.return_value = iter(file_contents.get(filepath, "").splitlines())
                mock_file_handle.read.return_value = file_contents.get(filepath, "")
                return mock_file_handle
        mock_file_open.side_effect = mock_open_side_effect

        result = scavenge_resources('/mock/dir', ['.txt'], 'report.txt')
        self.assertTrue(result) # The report should still be generated, just with an error for that file.
        report_content = ""
        for call_args in mock_file_open.return_value.write.call_args_list:
            report_content += call_args[0][0]
        self.assertIn("Error processing file: File not found", report_content)
        self.assertIn("Total files found matching criteria: 1", report_content)


if __name__ == '__main__':
    unittest.main()
