import unittest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
from src.collector import find_dust_files, main

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('pathlib.Path.is_dir', return_value=True) # Mock rationale: Simulate directory existence without actual filesystem interaction.
    def test_find_dust_files_empty_files(self, mock_is_dir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a directory structure with various files and sizes
        # without actually creating files on the filesystem.
        mock_walk.return_value = [
            ('/mock/dir', [], ['empty.txt', 'small.log', 'large.txt', 'another.tmp'])
        ]
        # Mock rationale: Control the reported size of each file for testing specific criteria.
        mock_getsize.side_effect = lambda p: {
            Path('/mock/dir/empty.txt'): 0,
            Path('/mock/dir/small.log'): 500,
            Path('/mock/dir/large.txt'): 2000,
            Path('/mock/dir/another.tmp'): 100,
        }.get(p, 0) # Default to 0 if path not found in mock, though it shouldn't happen here

        max_size = 1000 # 1KB
        extensions = ('.log', '.tmp')
        dust = find_dust_files(Path('/mock/dir'), max_size, extensions)

        expected_dust = [
            Path('/mock/dir/empty.txt'),
            Path('/mock/dir/small.log'),
            Path('/mock/dir/another.tmp'),
        ]
        self.assertCountEqual(dust, expected_dust)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_find_dust_files_no_dust(self, mock_is_dir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a directory where no files meet the 'dust' criteria.
        mock_walk.return_value = [
            ('/mock/dir', [], ['important.py', 'config.json', 'big_data.csv'])
        ]
        mock_getsize.side_effect = lambda p: {
            Path('/mock/dir/important.py'): 1500,
            Path('/mock/dir/config.json'): 1200,
            Path('/mock/dir/big_data.csv'): 50000,
        }.get(p, 0)

        max_size = 1000
        extensions = ('.log', '.tmp')
        dust = find_dust_files(Path('/mock/dir'), max_size, extensions)
        self.assertEqual(dust, [])

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_find_dust_files_mixed_criteria(self, mock_is_dir, mock_walk, mock_getsize):
        # Mock rationale: Test various combinations of size and extension criteria.
        mock_walk.return_value = [
            ('/mock/dir', ['subdir'], ['file1.log', 'file2.txt', 'file3.tmp', 'file4.bak']),
            ('/mock/dir/subdir', [], ['subfile1.log', 'subfile2.py', 'subfile3.empty'])
        ]
        mock_getsize.side_effect = lambda p: {
            Path('/mock/dir/file1.log'): 500,  # Dust: small, .log
            Path('/mock/dir/file2.txt'): 300,  # Not dust: small, but .txt (not in extensions)
            Path('/mock/dir/file3.tmp'): 1500, # Not dust: .tmp, but too large
            Path('/mock/dir/file4.bak'): 0,    # Dust: empty
            Path('/mock/dir/subdir/subfile1.log'): 900, # Dust: small, .log
            Path('/mock/dir/subdir/subfile2.py'): 2000, # Not dust: too large, .py
            Path('/mock/dir/subdir/subfile3.empty'): 0, # Dust: empty
        }.get(p, 0)

        max_size = 1000
        extensions = ('.log', '.bak')
        dust = find_dust_files(Path('/mock/dir'), max_size, extensions)

        expected_dust = [
            Path('/mock/dir/file1.log'),
            Path('/mock/dir/file4.bak'),
            Path('/mock/dir/subdir/subfile1.log'),
            Path('/mock/dir/subdir/subfile3.empty'),
        ]
        self.assertCountEqual(dust, expected_dust)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_find_dust_files_non_existent_file_during_scan(self, mock_is_dir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a file being deleted between os.walk and os.path.getsize call.
        mock_walk.return_value = [
            ('/mock/dir', [], ['existing.log', 'deleted.tmp'])
        ]
        def getsize_side_effect(p):
            if p == Path('/mock/dir/deleted.tmp'):
                raise FileNotFoundError
            return 100 # for existing.log
        mock_getsize.side_effect = getsize_side_effect

        max_size = 1000
        extensions = ('.log', '.tmp')
        dust = find_dust_files(Path('/mock/dir'), max_size, extensions)
        self.assertCountEqual(dust, [Path('/mock/dir/existing.log')])

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('pathlib.Path.is_dir', return_value=False) # Mock rationale: Simulate directory non-existence.
    def test_find_dust_files_non_existent_directory(self, mock_is_dir, mock_walk, mock_getsize):
        # Mock rationale: Test behavior when the target directory does not exist.
        dust = find_dust_files(Path('/non/existent/dir'), 1000, ('.log',))
        self.assertEqual(dust, [])
        mock_walk.assert_not_called() # os.walk should not be called if dir doesn't exist

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('src.collector.find_dust_files', return_value=[
        Path('/mock/dir/empty.txt'),
        Path('/mock/dir/small.log')
    ])
    @patch('os.path.getsize', side_effect=lambda p: {
        Path('/mock/dir/empty.txt'): 0,
        Path('/mock/dir/small.log'): 500,
    }.get(p, 0)) # Mock rationale: Provide sizes for reported files for output formatting.
    def test_main_with_dust(self, mock_getsize, mock_find_dust_files, mock_stdout):
        # Mock rationale: Test the main function's output when dust files are found.
        # We mock find_dust_files to control the output directly, and os.path.getsize
        # to provide realistic sizes for the print statements.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/mock/dir'),
            max_size=1000,
            extensions=".log,.tmp"
        )):
            main()
            output = mock_stdout.write.call_args_list
            output_str = "".join(call.args[0] for call in output)
            self.assertIn("Cosmic Dust Detected!", output_str)
            self.assertIn("- /mock/dir/empty.txt (0 bytes)", output_str)
            self.assertIn("- /mock/dir/small.log (500 bytes)", output_str)
            self.assertIn("Total 2 particles of cosmic dust found.", output_str)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('src.collector.find_dust_files', return_value=[]) # Mock rationale: Control the return value of find_dust_files to simulate no dust.
    def test_main_no_dust(self, mock_find_dust_files, mock_stdout):
        # Mock rationale: Test the main function's output when no dust files are found.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/mock/dir'),
            max_size=1000,
            extensions=".log,.tmp"
        )):
            main()
            output = mock_stdout.write.call_args_list
            output_str = "".join(call.args[0] for call in output)
            self.assertIn("No cosmic dust detected. Your digital cosmos is sparkling clean!", output_str)

if __name__ == '__main__':
    unittest.main()
