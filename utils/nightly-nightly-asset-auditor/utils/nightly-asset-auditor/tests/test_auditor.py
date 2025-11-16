import unittest
from unittest.mock import patch
import os
import sys

# Add the src directory to the path to allow importing auditor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import audit_directory, generate_report, format_size, get_file_extension, SURVIVAL_SCORES
sys.path.pop(0)

class TestAuditor(unittest.TestCase):

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension('file.txt'), '.txt')
        self.assertEqual(get_file_extension('archive.tar.gz'), '.gz')
        self.assertEqual(get_file_extension('noextensionfile'), '')
        self.assertEqual(get_file_extension('.gitignore'), '.gitignore') # Dotfile
        self.assertEqual(get_file_extension('folder/.hidden'), '.hidden') # Dotfile in folder
        self.assertEqual(get_file_extension('file.TXT'), '.txt') # Case insensitive
        self.assertEqual(get_file_extension('file.Py'), '.py') # Case insensitive

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_basic(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid directory.
        # os.walk is mocked to simulate a file system structure without actual disk access.
        # os.path.getsize is mocked to provide deterministic file sizes for testing calculations.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'doc.md']),
            ('/mock/dir/subdir', [], ['script.py', 'config.json'])
        ]
        mock_getsize.side_effect = {
            '/mock/dir/file1.txt': 100,
            '/mock/dir/doc.md': 200,
            '/mock/dir/subdir/script.py': 500,
            '/mock/dir/subdir/config.json': 300
        }.get

        total_files, total_size, file_type_stats = audit_directory('/mock/dir')

        self.assertEqual(total_files, 4)
        self.assertEqual(total_size, 100 + 200 + 500 + 300)

        self.assertIn('.txt', file_type_stats)
        self.assertEqual(file_type_stats['.txt']['count'], 1)
        self.assertEqual(file_type_stats['.txt']['size'], 100)
        self.assertEqual(file_type_stats['.txt']['score'], SURVIVAL_SCORES['.txt'])

        self.assertIn('.md', file_type_stats)
        self.assertEqual(file_type_stats['.md']['count'], 1)
        self.assertEqual(file_type_stats['.md']['size'], 200)
        self.assertEqual(file_type_stats['.md']['score'], SURVIVAL_SCORES['.md'])

        self.assertIn('.py', file_type_stats)
        self.assertEqual(file_type_stats['.py']['count'], 1)
        self.assertEqual(file_type_stats['.py']['size'], 500)
        self.assertEqual(file_type_stats['.py']['score'], SURVIVAL_SCORES['.py'])

        self.assertIn('.json', file_type_stats)
        self.assertEqual(file_type_stats['.json']['count'], 1)
        self.assertEqual(file_type_stats['.json']['size'], 300)
        self.assertEqual(file_type_stats['.json']['score'], SURVIVAL_SCORES['.json'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_multiple_files_same_type(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Same as above, simulating multiple files of the same type to test aggregation.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'file2.txt', 'file3.md'])
        ]
        mock_getsize.side_effect = {
            '/mock/dir/file1.txt': 100,
            '/mock/dir/file2.txt': 150,
            '/mock/dir/file3.md': 200
        }.get

        total_files, total_size, file_type_stats = audit_directory('/mock/dir')

        self.assertEqual(total_files, 3)
        self.assertEqual(total_size, 100 + 150 + 200)

        self.assertIn('.txt', file_type_stats)
        self.assertEqual(file_type_stats['.txt']['count'], 2)
        self.assertEqual(file_type_stats['.txt']['size'], 250)
        self.assertEqual(file_type_stats['.txt']['score'], SURVIVAL_SCORES['.txt'] * 2)

        self.assertIn('.md', file_type_stats)
        self.assertEqual(file_type_stats['.md']['count'], 1)
        self.assertEqual(file_type_stats['.md']['size'], 200)
        self.assertEqual(file_type_stats['.md']['score'], SURVIVAL_SCORES['.md'])

    @patch('os.path.isdir')
    def test_audit_directory_not_found(self, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to return False, simulating a non-existent directory.
        mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Directory not found"):n            audit_directory('/nonexistent/dir')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock/dir', [], ['unreadable.txt'])])
    @patch('os.path.getsize', side_effect=OSError('Permission denied'))
    def test_audit_directory_unreadable_file(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.getsize is mocked to raise an OSError, simulating an unreadable file.
        # This tests that the auditor handles such errors gracefully without crashing.
        total_files, total_size, file_type_stats = audit_directory('/mock/dir')
        self.assertEqual(total_files, 0) # Unreadable file should not be counted
        self.assertEqual(total_size, 0)
        self.assertEqual(file_type_stats, {})

    def test_format_size(self):
        self.assertEqual(format_size(0), '0 B')
        self.assertEqual(format_size(500), '500 B')
        self.assertEqual(format_size(1023), '1023 B')
        self.assertEqual(format_size(1024), '1.0 KB')
        self.assertEqual(format_size(1536), '1.5 KB')
        self.assertEqual(format_size(1024 * 1024), '1.0 MB')
        self.assertEqual(format_size(1.5 * 1024 * 1024), '1.5 MB')
        self.assertEqual(format_size(1024 * 1024 * 1024), '1.0 GB')

    def test_generate_report_empty(self):
        report = generate_report('/empty/dir', 0, 0, {})
        self.assertIn('Total Files Found: 0', report)
        self.assertIn('Total Size: 0 B', report)
        self.assertIn('Overall Apocalypse Readiness Score: 0', report)
        self.assertIn('File Type Breakdown:', report)

    def test_generate_report_full(self):
        directory_path = '/test/repo'
        total_files = 5
        total_size = 1024 * 1024 * 2.5 # 2.5 MB
        file_type_stats = {
            '.md': {'count': 2, 'size': 1024 * 100, 'score': SURVIVAL_SCORES['.md'] * 2},
            '.py': {'count': 2, 'size': 1024 * 500, 'score': SURVIVAL_SCORES['.py'] * 2},
            '.json': {'count': 1, 'size': 1024 * 1024 * 1.9, 'score': SURVIVAL_SCORES['.json'] * 1}
        }
        # Expected overall score: (10*2) + (8*2) + (6*1) = 20 + 16 + 6 = 42

        report = generate_report(directory_path, total_files, total_size, file_type_stats)

        self.assertIn(f"ApocalypsAI Digital Asset Audit Report for: {directory_path}", report)
        self.assertIn(f"Total Files Found: {total_files}", report)
        self.assertIn(f"Total Size: 2.5 MB", report)
        self.assertIn(f"Overall Apocalypse Readiness Score: 42", report)

        # Check breakdown lines and order (sorted by score descending, then extension ascending)
        lines = report.split('\n')
        # .md score 20, .py score 16, .json score 6
        # Expected order: .md, .py, .json
        md_line = f".md  : 2 files, 100.0 KB, Score: {SURVIVAL_SCORES['.md'] * 2:<3} (Survival Priority: High)"
        py_line = f".py  : 2 files, 500.0 KB, Score: {SURVIVAL_SCORES['.py'] * 2:<3} (Survival Priority: Medium)"
        json_line = f".json: 1 files, 1.9 MB, Score: {SURVIVAL_SCORES['.json'] * 1:<3} (Survival Priority: Medium)"

        self.assertIn(md_line, report)
        self.assertIn(py_line, report)
        self.assertIn(json_line, report)

        # Verify order by finding indices
        md_index = lines.index(md_line)
        py_index = lines.index(py_line)
        json_index = lines.index(json_line)

        self.assertTrue(md_index < py_index)
        self.assertTrue(py_index < json_index)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock/dir', [], ['file.log', 'important.md', 'script.sh'])])
    @patch('os.path.getsize', side_effect={'/mock/dir/file.log': 10, '/mock/dir/important.md': 20, '/mock/dir/script.sh': 30}.get)
    def test_report_sorting_by_score(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulates a directory with files of different survival scores to test report sorting.
        total_files, total_size, file_type_stats = audit_directory('/mock/dir')
        report = generate_report('/mock/dir', total_files, total_size, file_type_stats)

        lines = report.split('\n')
        # Expected order: .md (score 10), .sh (score 7), .log (score 1)
        md_line = f".md  : 1 files, 20 B, Score: {SURVIVAL_SCORES['.md'] * 1:<3} (Survival Priority: High)"
        sh_line = f".sh  : 1 files, 30 B, Score: {SURVIVAL_SCORES['.sh'] * 1:<3} (Survival Priority: Medium)"
        log_line = f".log : 1 files, 10 B, Score: {SURVIVAL_SCORES['.log'] * 1:<3} (Survival Priority: Very Low)"

        md_index = lines.index(md_line)
        sh_index = lines.index(sh_line)
        log_index = lines.index(log_line)

        self.assertTrue(md_index < sh_index)
        self.assertTrue(sh_index < log_index)

if __name__ == '__main__':
    unittest.main()
