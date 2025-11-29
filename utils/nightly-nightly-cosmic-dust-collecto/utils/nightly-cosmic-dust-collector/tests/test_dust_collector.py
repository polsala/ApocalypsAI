import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import collect_dust, main

class TestDustCollector(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_no_dust_found(self, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory structure where all files are larger than the threshold.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.log'])
        ]
        mock_getsize.side_effect = lambda x: 2048 if 'file1.txt' in x else 3072 # 2KB, 3KB

        dust = collect_dust('/root', max_size_kb=1) # Threshold 1KB
        self.assertEqual(len(dust), 0)

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_some_dust_found(self, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory with some small files that qualify as 'dust'.
        mock_walk.return_value = [
            ('/root', ['subdir'], ['small.txt', 'large.bin']),
            ('/root/subdir', [], ['empty.log', 'config.ini'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/root/small.txt': 512,  # 0.5KB
            '/root/large.bin': 5120, # 5KB
            '/root/subdir/empty.log': 0, # 0KB
            '/root/subdir/config.ini': 768 # 0.75KB
        }.get(x, 0)

        dust = collect_dust('/root', max_size_kb=1) # Threshold 1KB
        self.assertEqual(len(dust), 3)
        self.assertIn(('/root/small.txt', 0.5), dust)
        self.assertIn(('/root/subdir/empty.log', 0.0), dust)
        self.assertIn(('/root/subdir/config.ini', 0.75), dust)
        self.assertNotIn(('/root/large.bin', 5.0), dust)

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_empty_files_are_dust(self, mock_getsize, mock_walk):
        # Mock rationale: Ensure that files with 0 bytes are correctly identified as dust.
        mock_walk.return_value = [
            ('/root', [], ['zero.txt', 'non_zero.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/root/zero.txt': 0,
            '/root/non_zero.txt': 10240 # 10KB
        }.get(x, 0)

        dust = collect_dust('/root', max_size_kb=1)
        self.assertEqual(len(dust), 1)
        self.assertIn(('/root/zero.txt', 0.0), dust)

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_exclude_directories(self, mock_getsize, mock_walk):
        # Mock rationale: Verify that specified directories and their contents are skipped.
        mock_walk.return_value = [
            ('/root', ['.git', 'src', 'build'], ['file1.txt']),
            ('/root/.git', [], ['HEAD']),
            ('/root/src', [], ['main.py']),
            ('/root/build', [], ['output.log'])
        ]
        mock_getsize.side_effect = lambda x: 100 # All files are small

        dust = collect_dust('/root', max_size_kb=1, exclude_dirs=['.git', 'build'])
        self.assertEqual(len(dust), 2) # file1.txt and main.py should be found
        self.assertIn(('/root/file1.txt', 0.09765625), dust) # 100 bytes / 1024
        self.assertIn(('/root/src/main.py', 0.09765625), dust)
        self.assertNotIn(('/root/.git/HEAD', 0.09765625), dust)
        self.assertNotIn(('/root/build/output.log', 0.09765625), dust)

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_os_error_handling(self, mock_getsize, mock_walk):
        # Mock rationale: Ensure the collector handles files that become inaccessible during scan.
        mock_walk.return_value = [
            ('/root', [], ['accessible.txt', 'inaccessible.txt'])
        ]
        def getsize_side_effect(path):
            if 'inaccessible.txt' in path:
                raise OSError("Permission denied")
            return 100 # 0.1KB
        mock_getsize.side_effect = getsize_side_effect

        dust = collect_dust('/root', max_size_kb=1)
        self.assertEqual(len(dust), 1)
        self.assertIn(('/root/accessible.txt', 0.09765625), dust)
        self.assertNotIn(('/root/inaccessible.txt', 0.09766), dust)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_collector.collect_dust')
    def test_main_no_dust(self, mock_collect_dust, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's output when no dust is found.
        mock_parse_args.return_value = MagicMock(path='/test', max_size_kb=1, exclude=[])
        mock_collect_dust.return_value = []

        main()
        output = mock_stdout.getvalue()
        self.assertIn("No cosmic dust found. Your repository is sparkling clean!", output)
        self.assertIn("Scan complete. Total dust collected: 0 files.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_collector.collect_dust')
    def test_main_with_dust(self, mock_collect_dust, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's output when dust is found.
        mock_parse_args.return_value = MagicMock(path='/test', max_size_kb=1, exclude=[])
        mock_collect_dust.return_value = [
            ('/test/file1.txt', 0.1),
            ('/test/subdir/file2.log', 0.0)
        ]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Found 2 pieces of cosmic dust:", output)
        self.assertIn("- /test/file1.txt (0.1 KB)", output)
        self.assertIn("- /test/subdir/file2.log (0.0 KB)", output)
        self.assertIn("Scan complete. Total dust collected: 2 files.", output)

if __name__ == '__main__':
    unittest.main()
