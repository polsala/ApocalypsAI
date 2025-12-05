import unittest
import os
from unittest.mock import patch, mock_open
from src.mood_ring import get_file_mood

class TestFileMoodRing(unittest.TestCase):

    @patch('os.path.exists')
    def test_file_not_found(self, mock_exists):
        # Mock rationale: os.path.exists is an external dependency (filesystem state).
        # We mock it to simulate a non-existent file deterministically.
        mock_exists.return_value = False
        emoji, desc = get_file_mood('non_existent_file.txt')
        self.assertEqual(emoji, '❓')
        self.assertIn('File not found', desc)

    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_not_a_file(self, mock_isfile, mock_exists):
        # Mock rationale: os.path.exists and os.path.isfile are external dependencies.
        # We mock them to simulate a path that exists but is not a regular file (e.g., a directory).
        mock_exists.return_value = True
        mock_isfile.return_value = False
        emoji, desc = get_file_mood('a_directory/')
        self.assertEqual(emoji, '❓')
        self.assertIn('Not a regular file', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_empty_file(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide an empty string as file content deterministically.
        mock_file.return_value.read.return_value = ""
        emoji, desc = get_file_mood('empty.txt')
        self.assertEqual(emoji, '❓')
        self.assertIn('The file is empty', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_sparkling_serenity(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Sparkling Serenity' mood.
        mock_file.return_value.read.return_value = "This is a clean and simple file.\nIt contains success."
        emoji, desc = get_file_mood('clean_code.py')
        self.assertEqual(emoji, '✨')
        self.assertIn('Sparkling Serenity', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_fiery_frontier(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Fiery Frontier' mood.
        mock_file.return_value.read.return_value = (
            "TODO: Implement feature X\nFIXME: Bug in line 100\nBUG: Critical issue\n" +
            "Another TODO\nOne more TODO\nAnd a final TODO."
        )
        emoji, desc = get_file_mood('buggy_code.py')
        self.assertEqual(emoji, '🔥')
        self.assertIn('Fiery Frontier', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_critical_collapse(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Critical Collapse' mood.
        mock_file.return_value.read.return_value = (
            "ERROR: System crashed\nCRITICAL: Data loss detected\nERROR: Failed to initialize\n" +
            "This is a normal line."
        )
        emoji, desc = get_file_mood('critical_log.txt')
        self.assertEqual(emoji, '💀')
        self.assertIn('Critical Collapse', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_icy_inertia(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Icy Inertia' mood.
        mock_file.return_value.read.return_value = "This function is deprecated.\nConsider it stale.\nOld code."
        emoji, desc = get_file_mood('old_module.py')
        self.assertEqual(emoji, '🧊')
        self.assertIn('Icy Inertia', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_budding_bloom(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Budding Bloom' mood (short, no strong keywords).
        mock_file.return_value.read.return_value = "Hello world\nThis is a test.\nShort and sweet."
        emoji, desc = get_file_mood('short_script.sh')
        self.assertEqual(emoji, '🌿')
        self.assertIn('Budding Bloom', desc)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_under_construction(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to provide content that should trigger the 'Under Construction' mood (default/mixed).
        mock_file.return_value.read.return_value = (
            "This is a general file.\nIt has some content.\n" +
            "Maybe a few comments.\nLine four.\nLine five.\nLine six.\nLine seven.\nLine eight.\nLine nine.\nLine ten.\nLine eleven."
        )
        emoji, desc = get_file_mood('mixed_content.txt')
        self.assertEqual(emoji, '🚧')
        self.assertIn('Under Construction', desc)

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_read_error(self, mock_isfile, mock_exists, mock_file):
        # Mock rationale: builtins.open is an external dependency (filesystem I/O).
        # We mock it to raise an IOError, simulating a permission denied or other read error.
        emoji, desc = get_file_mood('unreadable.txt')
        self.assertEqual(emoji, '❓')
        self.assertIn('Could not read file', desc)

if __name__ == '__main__':
    unittest.main()
