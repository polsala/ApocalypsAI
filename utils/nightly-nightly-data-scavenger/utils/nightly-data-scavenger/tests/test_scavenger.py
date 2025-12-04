import unittest
from unittest.mock import patch, mock_open
import os
import json
from src.scavenger import scavenge_file, scavenge_directory, PREDEFINED_PATTERNS

class TestScavenger(unittest.TestCase):

    def test_scavenge_file_basic_pattern(self):
        # Mock rationale: Avoids actual file system access, ensuring deterministic and offline tests.
        mock_file_content = "This is a test file with a secret_key_123 and another_key_abc."
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as m_open:
            patterns = [r"secret_key_\d+"]
            matches = scavenge_file("dummy.txt", patterns)
            self.assertEqual(matches, ["secret_key_123"])
            m_open.assert_called_once_with("dummy.txt", 'r', encoding='utf-8', errors='ignore')

    def test_scavenge_file_multiple_patterns(self):
        # Mock rationale: Avoids actual file system access, ensuring deterministic and offline tests.
        mock_file_content = "Email: test@example.com. URL: http://example.org/path. Another email: user@domain.net"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as m_open:
            patterns = [PREDEFINED_PATTERNS['email'], PREDEFINED_PATTERNS['url']]
            matches = scavenge_file("dummy.txt", patterns)
            expected_matches = sorted(["test@example.com", "http://example.org/path", "user@domain.net"])
            self.assertEqual(matches, expected_matches)

    def test_scavenge_file_no_matches(self):
        # Mock rationale: Avoids actual file system access, ensuring deterministic and offline tests.
        mock_file_content = "No patterns here."
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as m_open:
            patterns = [r"non_existent_pattern"]
            matches = scavenge_file("dummy.txt", patterns)
            self.assertEqual(matches, [])

    def test_scavenge_file_empty_file(self):
        # Mock rationale: Avoids actual file system access, ensuring deterministic and offline tests.
        mock_file_content = ""
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as m_open:
            patterns = [r"any_pattern"]
            matches = scavenge_file("empty.txt", patterns)
            self.assertEqual(matches, [])

    def test_scavenge_file_io_error(self):
        # Mock rationale: Simulates file read errors without actual file system issues.
        with patch("builtins.open", side_effect=IOError("Permission denied")) as m_open:
            patterns = [r"any_pattern"]
            matches = scavenge_file("unreadable.txt", patterns)
            self.assertEqual(matches, []) # Should return empty list on error
            m_open.assert_called_once()

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=False)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_directory_basic(self, m_open, m_walk, m_isfile, m_isdir, m_exists):
        # Mock rationale: os.path.exists, os.path.isdir, os.path.isfile are mocked to simulate a file system structure
        # without creating actual files/directories. builtins.open is mocked to provide file content.
        m_walk.return_value = [
            ('root', ['subdir'], ['file1.txt']),
            ('root/subdir', [], ['file2.txt'])
        ]
        
        file_contents = {
            'root/file1.txt': 'This file has a URL: http://example.com',
            'root/subdir/file2.txt': 'This file has an email: user@test.org'
        }
        
        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError

        m_open.side_effect = mock_open_side_effect

        patterns = [PREDEFINED_PATTERNS['url'], PREDEFINED_PATTERNS['email']]
        results = scavenge_directory('root', patterns)

        expected_results = {
            'root/file1.txt': ['http://example.com'],
            'root/subdir/file2.txt': ['user@test.org']
        }
        self.assertEqual(results, expected_results)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_scavenge_directory_single_file(self, m_open, m_isfile, m_isdir, m_exists):
        # Mock rationale: os.path.exists, os.path.isdir and os.path.isfile are mocked to simulate a single file path.
        # builtins.open is mocked to provide file content.
        m_open.return_value.read.return_value = 'Only one file with email: single@file.com'
        patterns = [PREDEFINED_PATTERNS['email']]
        results = scavenge_directory('single_file.txt', patterns)
        expected_results = {'single_file.txt': ['single@file.com']}
        self.assertEqual(results, expected_results)

    @patch('os.path.exists', return_value=False)
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.isfile', return_value=False)
    def test_scavenge_directory_non_existent_path(self, m_isfile, m_isdir, m_exists):
        # Mock rationale: os.path.exists is mocked to simulate a non-existent path.
        patterns = [r"any"]
        with self.assertRaises(FileNotFoundError):
            scavenge_directory('non_existent', patterns)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=False)
    @patch('os.walk', return_value=[('root', [], ['file_no_match.txt'])])
    @patch('builtins.open', new_callable=mock_open, read_data='No relevant content')
    def test_scavenge_directory_no_matches_in_dir(self, m_open, m_walk, m_isfile, m_isdir, m_exists):
        # Mock rationale: os.walk is mocked to simulate a directory with a file, and builtins.open
        # provides content that doesn't match the patterns.
        patterns = [r"specific_match"]
        results = scavenge_directory('root', patterns)
        self.assertEqual(results, {})

    @patch('sys.stdout')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scavenge_directory')
    def test_main_with_patterns_and_types(self, mock_scavenge_directory, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # scavenge_directory is mocked to control the core logic's output. sys.stdout is mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            path='.',
            patterns=['custom_pattern'],
            types=['url']
        )
        mock_scavenge_directory.return_value = {
            './file.txt': ['http://example.com', 'custom_match']
        }

        from src.scavenger import main
        main()

        mock_scavenge_directory.assert_called_once()
        args, kwargs = mock_scavenge_directory.call_args
        self.assertEqual(args[0], '.') # path
        self.assertIn('custom_pattern', args[1])
        self.assertIn(PREDEFINED_PATTERNS['url'], args[1])
        mock_stdout.write.assert_called_once_with(json.dumps({
            './file.txt': ['http://example.com', 'custom_match']
        }, indent=2) + '\n')

    @patch('sys.stdout')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scavenge_directory')
    def test_main_no_patterns_or_types(self, mock_scavenge_directory, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # sys.stdout is mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            path='.',
            patterns=[],
            types=[]
        )

        from src.scavenger import main
        main()

        mock_scavenge_directory.assert_not_called()
        mock_stdout.write.assert_called_once_with(json.dumps({}) + '\n')

    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scavenge_directory', side_effect=FileNotFoundError('Path not found'))
    def test_main_file_not_found_error(self, mock_scavenge_directory, mock_parse_args, mock_exit, mock_stderr):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # scavenge_directory is mocked to simulate a FileNotFoundError. sys.stderr and sys.exit are mocked
        # to capture error output and prevent actual program exit.
        mock_parse_args.return_value = argparse.Namespace(
            path='non_existent_path',
            patterns=['test'],
            types=[]
        )

        from src.scavenger import main
        main()

        mock_scavenge_directory.assert_called_once()
        mock_stderr.write.assert_called_once_with(json.dumps({"error": "Path not found"}) + '\n')
        mock_exit.assert_called_once_with(1)

    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scavenge_directory', side_effect=ValueError('Not a file or directory'))
    def test_main_value_error(self, mock_scavenge_directory, mock_parse_args, mock_exit, mock_stderr):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # scavenge_directory is mocked to simulate a ValueError. sys.stderr and sys.exit are mocked
        # to capture error output and prevent actual program exit.
        mock_parse_args.return_value = argparse.Namespace(
            path='/dev/null/not-a-real-path',
            patterns=['test'],
            types=[]
        )

        from src.scavenger import main
        main()

        mock_scavenge_directory.assert_called_once()
        mock_stderr.write.assert_called_once_with(json.dumps({"error": "Not a file or directory"}) + '\n')
        mock_exit.assert_called_once_with(1)
