import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing linker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import linker

class TestNightlyQuantumLinker(unittest.TestCase):

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open, mock_isfile):
        # Mock rationale: os.path.isfile to confirm file existence, builtins.open to simulate file content.
        mock_file_open.return_value.read.side_effect = [b'content1', b'content2', b'']
        expected_hash = hashlib.sha256(b'content1content2').hexdigest()
        self.assertEqual(linker.calculate_file_hash('/fake/path/file.txt'), expected_hash)

        mock_file_open.return_value.read.side_effect = [b'unique_content', b'']
        expected_hash_unique = hashlib.sha256(b'unique_content').hexdigest()
        self.assertEqual(linker.calculate_file_hash('/fake/path/unique.txt'), expected_hash_unique)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates(self, mock_file_open, mock_isfile, mock_walk):
        # Mock rationale: os.walk to simulate directory structure, os.path.isfile to confirm file existence,
        # builtins.open to simulate file content for hashing.

        # Simulate a directory structure with duplicates
        mock_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt', 'fileC.txt']),
            ('/root/subdir', [], ['fileD.txt', 'fileE.txt'])
        ]

        # Simulate file contents for hashing
        # fileA.txt and fileD.txt are duplicates
        # fileB.txt and fileE.txt are duplicates
        # fileC.txt is unique
        file_contents = {
            '/root/fileA.txt': b'duplicate_content_1',
            '/root/fileB.txt': b'duplicate_content_2',
            '/root/fileC.txt': b'unique_content_3',
            '/root/subdir/fileD.txt': b'duplicate_content_1',
            '/root/subdir/fileE.txt': b'duplicate_content_2',
        }

        def mock_read_content(filepath, mode='rb'):
            m = mock_open(read_data=file_contents[filepath])
            m.return_value.__enter__.return_value.read.side_effect = [file_contents[filepath], b'']
            return m()
        mock_file_open.side_effect = mock_read_content

        duplicates = linker.find_duplicates('/root')

        hash1 = hashlib.sha256(b'duplicate_content_1').hexdigest()
        hash2 = hashlib.sha256(b'duplicate_content_2').hexdigest()

        self.assertIn(hash1, duplicates)
        self.assertIn(hash2, duplicates)
        self.assertNotIn(hashlib.sha256(b'unique_content_3').hexdigest(), duplicates)

        self.assertCountEqual(duplicates[hash1], ['/root/fileA.txt', '/root/subdir/fileD.txt'])
        self.assertCountEqual(duplicates[hash2], ['/root/fileB.txt', '/root/subdir/fileE.txt'])

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=100) # Mock file size for calculation
    @patch('os.remove')
    @patch('os.link')
    @patch('os.stat')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    def test_link_duplicates_dry_run(self, mock_stdout, mock_stat, mock_link, mock_remove, mock_getsize, mock_file_open, mock_isfile, mock_walk):
        # Mock rationale: os.walk, os.path.isfile, builtins.open for finding duplicates.
        # os.path.getsize for calculating saved space. os.remove, os.link to ensure they are NOT called in dry-run.
        # os.stat to simulate inode information (different for original/duplicate initially).
        # sys.stdout to capture output for verification.

        mock_walk.return_value = [
            ('/root', [], ['orig1.txt', 'dup1_1.txt', 'orig2.txt', 'dup2_1.txt'])
        ]

        file_contents = {
            '/root/orig1.txt': b'content_A',
            '/root/dup1_1.txt': b'content_A',
            '/root/orig2.txt': b'content_B',
            '/root/dup2_1.txt': b'content_B',
        }

        def mock_read_content(filepath, mode='rb'):
            m = mock_open(read_data=file_contents[filepath])
            m.return_value.__enter__.return_value.read.side_effect = [file_contents[filepath], b'']
            return m()
        mock_file_open.side_effect = mock_read_content

        # Mock os.stat to return different inodes for original and duplicate initially
        # and then the same inode for the original and the *would-be-linked* duplicate
        # This simulates the state before and after linking.
        original_inode_1 = 1001
        duplicate_inode_1 = 1002
        original_inode_2 = 2001
        duplicate_inode_2 = 2002

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if path == '/root/orig1.txt':
                mock_stat_obj.st_ino = original_inode_1
            elif path == '/root/dup1_1.txt':
                mock_stat_obj.st_ino = duplicate_inode_1
            elif path == '/root/orig2.txt':
                mock_stat_obj.st_ino = original_inode_2
            elif path == '/root/dup2_1.txt':
                mock_stat_obj.st_ino = duplicate_inode_2
            else:
                mock_stat_obj.st_ino = 9999 # Unique inode for other files
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        linker.link_duplicates('/root', dry_run=True)

        mock_remove.assert_not_called()
        mock_link.assert_not_called()

        # Check output for dry run messages
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("[DRY RUN] Would remove '/root/dup1_1.txt' and hard-link to '/root/orig1.txt'.", output_str)
        self.assertIn("[DRY RUN] Would remove '/root/dup2_1.txt' and hard-link to '/root/orig2.txt'.", output_str)
        self.assertIn("[DRY RUN SUMMARY] Would have linked 2 files, saving approximately 0.00 MB.", output_str) # 100 bytes is 0.00 MB

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=100) # Mock file size for calculation
    @patch('os.remove')
    @patch('os.link')
    @patch('os.stat')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    def test_link_duplicates_actual_run(self, mock_stdout, mock_stat, mock_link, mock_remove, mock_getsize, mock_file_open, mock_isfile, mock_walk):
        # Mock rationale: os.walk, os.path.isfile, builtins.open for finding duplicates.
        # os.path.getsize for calculating saved space. os.remove, os.link to verify actual calls.
        # os.stat to simulate inode information (different for original/duplicate initially).
        # sys.stdout to capture output for verification.

        mock_walk.return_value = [
            ('/root', [], ['orig1.txt', 'dup1_1.txt', 'orig2.txt', 'dup2_1.txt'])
        ]

        file_contents = {
            '/root/orig1.txt': b'content_A',
            '/root/dup1_1.txt': b'content_A',
            '/root/orig2.txt': b'content_B',
            '/root/dup2_1.txt': b'content_B',
        }

        def mock_read_content(filepath, mode='rb'):
            m = mock_open(read_data=file_contents[filepath])
            m.return_value.__enter__.return_value.read.side_effect = [file_contents[filepath], b'']
            return m()
        mock_file_open.side_effect = mock_read_content

        # Mock os.stat to return different inodes for original and duplicate initially
        original_inode_1 = 1001
        duplicate_inode_1 = 1002
        original_inode_2 = 2001
        duplicate_inode_2 = 2002

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if path == '/root/orig1.txt':
                mock_stat_obj.st_ino = original_inode_1
            elif path == '/root/dup1_1.txt':
                mock_stat_obj.st_ino = duplicate_inode_1
            elif path == '/root/orig2.txt':
                mock_stat_obj.st_ino = original_inode_2
            elif path == '/root/dup2_1.txt':
                mock_stat_obj.st_ino = duplicate_inode_2
            else:
                mock_stat_obj.st_ino = 9999 # Unique inode for other files
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        linker.link_duplicates('/root', dry_run=False)

        mock_remove.assert_any_call('/root/dup1_1.txt')
        mock_link.assert_any_call('/root/orig1.txt', '/root/dup1_1.txt')
        mock_remove.assert_any_call('/root/dup2_1.txt')
        mock_link.assert_any_call('/root/orig2.txt', '/root/dup2_1.txt')

        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_link.call_count, 2)

        # Check output for actual run messages
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("Removed '/root/dup1_1.txt' and hard-linked to '/root/orig1.txt'.", output_str)
        self.assertIn("Removed '/root/dup2_1.txt' and hard-linked to '/root/orig2.txt'.", output_str)
        self.assertIn("[SUMMARY] Successfully linked 2 files, saving approximately 0.00 MB.", output_str)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=100)
    @patch('os.remove')
    @patch('os.link')
    @patch('os.stat')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_link_duplicates_already_linked(self, mock_stdout, mock_stat, mock_link, mock_remove, mock_getsize, mock_file_open, mock_isfile, mock_walk):
        # Mock rationale: Test scenario where duplicates are already hard-linked.

        mock_walk.return_value = [
            ('/root', [], ['orig.txt', 'dup.txt'])
        ]

        file_contents = {
            '/root/orig.txt': b'content_A',
            '/root/dup.txt': b'content_A',
        }

        def mock_read_content(filepath, mode='rb'):
            m = mock_open(read_data=file_contents[filepath])
            m.return_value.__enter__.return_value.read.side_effect = [file_contents[filepath], b'']
            return m()
        mock_file_open.side_effect = mock_read_content

        # Mock os.stat to return the SAME inode for original and duplicate
        shared_inode = 1001
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_ino = shared_inode
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        linker.link_duplicates('/root', dry_run=False)

        mock_remove.assert_not_called()
        mock_link.assert_not_called()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("'dup.txt' is already hard-linked to '/root/orig.txt'. Skipping.", output_str)
        self.assertIn("Successfully linked 0 files", output_str)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=100)
    @patch('os.remove')
    @patch('os.link')
    @patch('os.stat')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_link_duplicates_no_duplicates(self, mock_stdout, mock_stat, mock_link, mock_remove, mock_getsize, mock_file_open, mock_isfile, mock_walk):
        # Mock rationale: Test scenario with no duplicates found.

        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt'])
        ]

        file_contents = {
            '/root/file1.txt': b'content_A',
            '/root/file2.txt': b'content_B',
        }

        def mock_read_content(filepath, mode='rb'):
            m = mock_open(read_data=file_contents[filepath])
            m.return_value.__enter__.return_value.read.side_effect = [file_contents[filepath], b'']
            return m()
        mock_file_open.side_effect = mock_read_content

        linker.link_duplicates('/root', dry_run=False)

        mock_remove.assert_not_called()
        mock_link.assert_not_called()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("No duplicate files found. Disk space is optimally entangled!", output_str)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_invalid_dir(self, mock_stderr, mock_exit, mock_isdir):
        # Mock rationale: os.path.isdir to simulate an invalid directory.
        # sys.exit to prevent actual exit during test. sys.stderr to capture error output.
        with patch('sys.argv', ['linker.py', '--dir', '/nonexistent']):
            linker.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Directory '/nonexistent' not found or is not a directory.", mock_stderr.write.call_args[0][0])

    @patch('os.path.isdir', return_value=True)
    @patch('linker.link_duplicates')
    def test_main_valid_dir(self, mock_link_duplicates, mock_isdir):
        # Mock rationale: os.path.isdir to simulate a valid directory.
        # linker.link_duplicates to ensure the core logic is called with correct arguments.
        with patch('sys.argv', ['linker.py', '--dir', '/valid/path']):
            linker.main()
            mock_link_duplicates.assert_called_once_with('/valid/path', False)

        with patch('sys.argv', ['linker.py', '--dir', '/valid/path', '--dry-run']):
            linker.main()
            mock_link_duplicates.assert_called_once_with('/valid/path', True)

if __name__ == '__main__':
    unittest.main()
