import unittest
from unittest.mock import patch, mock_open
import os
import sys
from datetime import datetime

# Add the src directory to the path to allow importing auditor.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import AssetAuditor, SURVIVAL_SCORES

class TestAssetAuditor(unittest.TestCase):

    def setUp(self):
        self.mock_base_path = '/mock/repo'

    @patch('os.path.isdir')
    def test_auditor_init_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory for initialization test.
        mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Directory not found"): 
            AssetAuditor('/nonexistent/path')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    def test_auditor_empty_directory(self, mock_isfile, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory to ensure correct handling of no files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_base_path, [], [])
        ]
        mock_getsize.return_value = 0 # Not called in this scenario, but good practice
        mock_isfile.return_value = True

        auditor = AssetAuditor(self.mock_base_path)
        auditor.audit()

        self.assertEqual(auditor.total_files, 0)
        self.assertEqual(auditor.total_size, 0)
        self.assertEqual(auditor.file_stats, {})

        report = auditor.generate_report()
        self.assertIn("Total Files Scanned: 0", report)
        self.assertIn("Total Size Scanned: 0 B", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    def test_auditor_basic_scan(self, mock_isfile, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with various files and sizes to test core scanning logic.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_base_path, ['sub1'], ['file1.py', 'doc.md', 'log.txt']),
            (os.path.join(self.mock_base_path, 'sub1'), [], ['config.yml', 'temp.tmp'])
        ]

        # Map file paths to sizes
        file_sizes = {
            os.path.join(self.mock_base_path, 'file1.py'): 1000,
            os.path.join(self.mock_base_path, 'doc.md'): 500,
            os.path.join(self.mock_base_path, 'log.txt'): 2000,
            os.path.join(self.mock_base_path, 'sub1', 'config.yml'): 200,
            os.path.join(self.mock_base_path, 'sub1', 'temp.tmp'): 100,
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)
        mock_isfile.return_value = True

        auditor = AssetAuditor(self.mock_base_path)
        auditor.audit()

        self.assertEqual(auditor.total_files, 5)
        self.assertEqual(auditor.total_size, 1000 + 500 + 2000 + 200 + 100)

        self.assertIn('.py', auditor.file_stats)
        self.assertEqual(auditor.file_stats['.py']['count'], 1)
        self.assertEqual(auditor.file_stats['.py']['size'], 1000)
        self.assertEqual(auditor.file_stats['.py']['score'], SURVIVAL_SCORES['.py'])

        self.assertIn('.md', auditor.file_stats)
        self.assertEqual(auditor.file_stats['.md']['count'], 1)
        self.assertEqual(auditor.file_stats['.md']['size'], 500)
        self.assertEqual(auditor.file_stats['.md']['score'], SURVIVAL_SCORES['.md'])

        self.assertIn('.txt', auditor.file_stats)
        self.assertEqual(auditor.file_stats['.txt']['count'], 1)
        self.assertEqual(auditor.file_stats['.txt']['size'], 2000)
        self.assertEqual(auditor.file_stats['.txt']['score'], SURVIVAL_SCORES['.txt'])

        self.assertIn('.yml', auditor.file_stats)
        self.assertEqual(auditor.file_stats['.yml']['count'], 1)
        self.assertEqual(auditor.file_stats['.yml']['size'], 200)
        self.assertEqual(auditor.file_stats['.yml']['score'], SURVIVAL_SCORES['.yml'])

        self.assertIn('.tmp', auditor.file_stats)
        self.assertEqual(auditor.file_stats['.tmp']['count'], 1)
        self.assertEqual(auditor.file_stats['.tmp']['size'], 100)
        self.assertEqual(auditor.file_stats['.tmp']['score'], SURVIVAL_SCORES['.tmp'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    def test_auditor_report_generation(self, mock_isfile, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test the formatting and content of the generated Markdown report.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_base_path, [], ['main.py', 'README.md', 'data.csv', 'temp.bak', 'noext'])
        ]
        file_sizes = {
            os.path.join(self.mock_base_path, 'main.py'): 1500,
            os.path.join(self.mock_base_path, 'README.md'): 800,
            os.path.join(self.mock_base_path, 'data.csv'): 3000,
            os.path.join(self.mock_base_path, 'temp.bak'): 200,
            os.path.join(self.mock_base_path, 'noext'): 100,
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)
        mock_isfile.return_value = True

        auditor = AssetAuditor(self.mock_base_path)
        auditor.audit()
        report = auditor.generate_report()

        self.assertIn(f"# Digital Asset Audit Report: {self.mock_base_path}", report)
        self.assertIn("| File Type | Count | Total Size | Survival Score | Notes |", report)
        self.assertIn("| .py | 1 | 1.5 KB | 5 (Critical) | |", report)
        self.assertIn("| .md | 1 | 800 B | 5 (Critical) | |", report)
        self.assertIn("| .csv | 1 | 2.9 KB | 3 (Useful) | |", report)
        self.assertIn("| .bak | 1 | 200 B | 1 (Disposable) | |", report)
        self.assertIn("| (No Extension) | 1 | 100 B | 0 (Irrelevant) | |", report)
        self.assertIn("Total Files Scanned: 5", report)
        self.assertIn("Total Size Scanned: 5.5 KB", report)

        # Ensure sorting by score (desc) then type (asc)
        lines = report.split('\n')
        # Find the start of the table data
        table_start_idx = -1
        for i, line in enumerate(lines):
            if line.startswith('| :--------'):
                table_start_idx = i + 1
                break
        self.assertNotEqual(table_start_idx, -1, "Could not find table start in report")

        table_rows = []
        for i in range(table_start_idx, len(lines)):
            if lines[i].startswith('| '):
                table_rows.append(lines[i])
            else:
                break
        
        # Expected order: .py, .md (score 5), .csv (score 3), .bak (score 1), (No Extension) (score 0)
        self.assertGreaterEqual(len(table_rows), 5)
        self.assertIn(".py", table_rows[0])
        self.assertIn(".md", table_rows[1])
        self.assertIn(".csv", table_rows[2])
        self.assertIn(".bak", table_rows[3])
        self.assertIn("(No Extension)", table_rows[4])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('sys.stderr', new_callable=mock_open)
    def test_auditor_file_access_error(self, mock_stderr, mock_isfile, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file that cannot be accessed during the scan to test error handling.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_base_path, [], ['good.py', 'bad.txt'])
        ]
        
        def getsize_side_effect(path):
            if 'bad.txt' in path:
                raise OSError("Permission denied")
            return 100

        mock_getsize.side_effect = getsize_side_effect
        mock_isfile.return_value = True

        auditor = AssetAuditor(self.mock_base_path)
        auditor.audit()

        # 'bad.txt' should not be counted
        self.assertEqual(auditor.total_files, 1)
        self.assertEqual(auditor.total_size, 100)
        self.assertIn('.py', auditor.file_stats)
        self.assertNotIn('.txt', auditor.file_stats)

        # Check if warning was printed to stderr
        mock_stderr().write.assert_called_with(unittest.mock.ANY)
        self.assertIn("Warning: Could not access file", mock_stderr().write.call_args[0][0])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    def test_auditor_symlink_handling(self, mock_isfile, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Ensure that non-regular files (like broken symlinks) are skipped.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_base_path, [], ['regular.py', 'broken_link.txt'])
        ]
        
        def isfile_side_effect(path):
            if 'broken_link.txt' in path:
                return False # Simulate a non-regular file (e.g., broken symlink)
            return True

        mock_isfile.side_effect = isfile_side_effect
        mock_getsize.return_value = 100 # Only for regular.py

        auditor = AssetAuditor(self.mock_base_path)
        auditor.audit()

        self.assertEqual(auditor.total_files, 1)
        self.assertEqual(auditor.total_size, 100)
        self.assertIn('.py', auditor.file_stats)
        self.assertNotIn('.txt', auditor.file_stats)

if __name__ == '__main__':
    unittest.main()
