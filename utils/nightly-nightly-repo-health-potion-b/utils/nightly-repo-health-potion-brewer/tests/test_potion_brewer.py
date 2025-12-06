import unittest
from unittest.mock import patch, mock_open
import os
from src.potion_brewer import check_repo_health

class TestPotionBrewer(unittest.TestCase):

    def setUp(self):
        # Mock the current working directory for consistent testing
        self.mock_repo_path = '/mock/repo'

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_files_present_and_contributing_not_placeholder(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository where all essential files exist
        # and CONTRIBUTING.md has meaningful content.
        mock_exists.side_effect = lambda p: p in [
            os.path.join(self.mock_repo_path, 'README.md'),
            os.path.join(self.mock_repo_path, 'LICENSE'),
            os.path.join(self.mock_repo_path, '.gitignore'),
            os.path.join(self.mock_repo_path, 'CHANGELOG.md'),
            os.path.join(self.mock_repo_path, 'CONTRIBUTING.md'),
        ]
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'Meaningful contribution guidelines.'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_readme(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository missing only README.md.
        mock_exists.side_effect = lambda p: p != os.path.join(self.mock_repo_path, 'README.md')
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'Meaningful content.' # For CONTRIBUTING.md

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Missing Readme of Lore')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_license(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository missing only LICENSE.
        mock_exists.side_effect = lambda p: p != os.path.join(self.mock_repo_path, 'LICENSE')
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'Meaningful content.'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Absence of Legal Charm')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_gitignore(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository missing only .gitignore.
        mock_exists.side_effect = lambda p: p != os.path.join(self.mock_repo_path, '.gitignore')
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'Meaningful content.'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Unfiltered Artifacts')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_changelog(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository missing only CHANGELOG.md.
        mock_exists.side_effect = lambda p: p != os.path.join(self.mock_repo_path, 'CHANGELOG.md')
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'Meaningful content.'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Forgotten Changelog')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_contributing_is_placeholder(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository where CONTRIBUTING.md exists but contains placeholder text.
        mock_exists.side_effect = lambda p: p in [
            os.path.join(self.mock_repo_path, 'README.md'),
            os.path.join(self.mock_repo_path, 'LICENSE'),
            os.path.join(self.mock_repo_path, '.gitignore'),
            os.path.join(self.mock_repo_path, 'CHANGELOG.md'),
            os.path.join(self.mock_repo_path, 'CONTRIBUTING.md'),
        ]
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'TODO: Add contribution guidelines here.'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Silent Contribution Scroll')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_contributing_is_empty(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository where CONTRIBUTING.md exists but is empty.
        mock_exists.side_effect = lambda p: p in [
            os.path.join(self.mock_repo_path, 'README.md'),
            os.path.join(self.mock_repo_path, 'LICENSE'),
            os.path.join(self.mock_repo_path, '.gitignore'),
            os.path.join(self.mock_repo_path, 'CHANGELOG.md'),
            os.path.join(self.mock_repo_path, 'CONTRIBUTING.md'),
        ]
        mock_file_open.return_value.__enter__.return_value.read.return_value = ''

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 1)
        self.assertEqual(ailments[0]['ailment'], 'Silent Contribution Scroll')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_ailments(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository missing multiple files and having a placeholder CONTRIBUTING.md.
        mock_exists.side_effect = lambda p: p in [
            os.path.join(self.mock_repo_path, 'CONTRIBUTING.md'), # Only this one exists
        ]
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'TBD'

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 5) # All 5 ailments should be detected
        expected_ailments = {
            'Missing Readme of Lore',
            'Absence of Legal Charm',
            'Unfiltered Artifacts',
            'Forgotten Changelog',
            'Silent Contribution Scroll'
        }
        actual_ailments = {a['ailment'] for a in ailments}
        self.assertEqual(actual_ailments, expected_ailments)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_contributing_file_read_error(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a repository where CONTRIBUTING.md exists but cannot be read (e.g., permission error).
        # The utility should gracefully handle this and not report it as a placeholder if it can't confirm.
        mock_exists.side_effect = lambda p: p in [
            os.path.join(self.mock_repo_path, 'README.md'),
            os.path.join(self.mock_repo_path, 'LICENSE'),
            os.path.join(self.mock_repo_path, '.gitignore'),
            os.path.join(self.mock_repo_path, 'CHANGELOG.md'),
            os.path.join(self.mock_repo_path, 'CONTRIBUTING.md'),
        ]
        mock_file_open.side_effect = IOError("Permission denied")

        ailments = check_repo_health(self.mock_repo_path)
        self.assertEqual(len(ailments), 0) # No ailments should be reported if all other files exist and CONTRIBUTING.md can't be read

if __name__ == '__main__':
    unittest.main()
