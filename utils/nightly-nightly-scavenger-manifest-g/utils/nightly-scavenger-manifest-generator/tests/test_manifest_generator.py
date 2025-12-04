import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manifest_generator import generate_manifest

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_basic_manifest_generation(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate a directory structure with files for scanning.
        mock_walk.return_value = [
            ('/mock_dir', ('subdir1',), ('file1.txt', 'file2.log')),
            ('/mock_dir/subdir1', (), ('subfile.json',))
        ]
        
        # Mock rationale: Provide deterministic file sizes for the mocked files.
        mock_getsize.side_effect = lambda p: {
            '/mock_dir/file1.txt': 100,
            '/mock_dir/file2.log': 250,
            '/mock_dir/subdir1/subfile.json': 50
        }.get(p, 0)

        # Mock rationale: Simulate reading file content for snippets. The sequence matches calls to open().
        mock_file_open.side_effect = [
            mock_open(read_data='content of file1.txt').return_value, # For file1.txt
            mock_open(read_data='log data for file2.log').return_value, # For file2.log
            mock_open(read_data='json content').return_value, # For subfile.json
            mock_open().return_value # For writing the output manifest
        ]

        output_path = '/output/manifest.md'
        generate_manifest('/mock_dir', [], output_path, snippet_length=10)

        # Assert that the output file was opened for writing
        mock_file_open.assert_called_with(output_path, 'w', encoding='utf-8')
        
        # Get the content written to the output file
        written_content = mock_file_open().write.call_args[0][0]
        
        # Expected content (order might vary based on os.walk, but we'll check for presence)
        self.assertIn("# Scavenger's Manifest", written_content)
        self.assertIn("| Path | Size (bytes) | Snippet |", written_content)
        self.assertIn("| :--- | :----------: | :------ |", written_content)
        self.assertIn("`/mock_dir/file1.txt` | 100 | `content of...` |", written_content)
        self.assertIn("`/mock_dir/file2.log` | 250 | `log data f...` |", written_content)
        self.assertIn("`/mock_dir/subdir1/subfile.json` | 50 | `json conte...` |", written_content)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_filter_by_patterns(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate a directory structure with files for scanning.
        mock_walk.return_value = [
            ('/mock_dir', (), ('report.txt', 'data.json', 'image.png'))
        ]
        
        # Mock rationale: Provide deterministic file sizes for the mocked files.
        mock_getsize.side_effect = lambda p: {
            '/mock_dir/report.txt': 120,
            '/mock_dir/data.json': 80,
            '/mock_dir/image.png': 500
        }.get(p, 0)

        # Mock rationale: Simulate reading file content for snippets. The sequence matches calls to open().
        mock_file_open.side_effect = [
            mock_open(read_data='report content').return_value, # For report.txt
            mock_open(read_data='json content').return_value, # For data.json
            mock_open().return_value # For writing the output manifest
        ]

        output_path = '/output/filtered_manifest.md'
        generate_manifest('/mock_dir', ['*.txt', '*.json'], output_path, snippet_length=10)

        written_content = mock_file_open().write.call_args[0][0]

        self.assertIn("`/mock_dir/report.txt` | 120 | `report con...` |", written_content)
        self.assertIn("`/mock_dir/data.json` | 80 | `json conte...` |", written_content)
        self.assertNotIn("image.png", written_content)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_snippet_generation(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate a directory structure with files for scanning.
        mock_walk.return_value = [
            ('/mock_dir', (), ('simple.txt',))
        ]
        
        # Mock rationale: Provide deterministic file sizes for the mocked files.
        mock_getsize.return_value = 42

        # Mock rationale: Only need to mock the output file open, as no input files will be read for snippets.
        mock_file_open.return_value = mock_open().return_value

        output_path = '/output/no_snippet.md'
        generate_manifest('/mock_dir', [], output_path, snippet_length=0)

        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn("`/mock_dir/simple.txt` | 42 | `` |", written_content)
        # Ensure no read calls were made for snippets
        self.assertEqual(mock_file_open.call_count, 1) # Only for writing output

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_directory(self, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate an empty directory structure.
        mock_walk.return_value = [
            ('/mock_dir', (), ())
        ]
        
        # Mock rationale: Only need to mock the output file open.
        mock_file_open.return_value = mock_open().return_value

        output_path = '/output/empty.md'
        generate_manifest('/mock_dir', [], output_path)

        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn("No matching files found in '/mock_dir' with patterns all files.", written_content)

    @patch('os.path.isdir')
    @patch('builtins.print') # Mock rationale: Capture print statements for error messages
    def test_directory_not_found(self, mock_print, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        
        with self.assertRaises(FileNotFoundError) as cm:
            generate_manifest('/non_existent_dir', [], '/output/manifest.md')
        self.assertIn("Directory not found: /non_existent_dir", str(cm.exception))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_read_error_handling(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate a directory structure with files for scanning.
        mock_walk.return_value = [
            ('/mock_dir', (), ('unreadable.txt',))
        ]
        
        # Mock rationale: Provide deterministic file sizes for the mocked files.
        mock_getsize.return_value = 100

        # Mock rationale: Simulate an IOError when trying to open a file for reading, then mock the output file.
        mock_file_open.side_effect = [
            IOError("Permission denied"), # For unreadable.txt
            mock_open().return_value # For writing the output manifest
        ]

        output_path = '/output/error_manifest.md'
        
        # We expect a warning to be printed, but the function should not crash
        with patch('builtins.print') as mock_print:
            generate_manifest('/mock_dir', [], output_path, snippet_length=10)
            mock_print.assert_called_with("Warning: Could not process /mock_dir/unreadable.txt: Permission denied")

        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn("# Scavenger's Manifest", written_content)
        self.assertNotIn("unreadable.txt", written_content) # Should not be in the manifest if it couldn't be processed

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_markdown_escaping(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate a directory structure with files containing markdown special characters.
        mock_walk.return_value = [
            ('/mock_dir', (), ('file|with|pipes.txt',))
        ]
        
        # Mock rationale: Provide deterministic file sizes for the mocked files.
        mock_getsize.return_value = 70

        # Mock rationale: Simulate reading file content with markdown special characters, then mock the output file.
        mock_file_open.side_effect = [
            mock_open(read_data='content with | pipes and\nnewlines').return_value, # For file|with|pipes.txt
            mock_open().return_value # For writing the output manifest
        ]

        output_path = '/output/escaped_manifest.md'
        generate_manifest('/mock_dir', [], output_path, snippet_length=20)

        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn("`/mock_dir/file\\|with\\|pipes.txt` | 70 | `content with \\| p...` |", written_content)


if __name__ == '__main__':
    unittest.main()
