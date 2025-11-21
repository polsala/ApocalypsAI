import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_walk):
        # Mock rationale: Simulate a file system structure without creating actual files.
        mock_walk.return_value = [
            ('/repo', ('dir1', 'dir2'), ('README.md', 'file.txt')),
            ('/repo/dir1', (), ('doc.md', 'image.png')),
            ('/repo/dir2', ('subdir'), ('another.md',)),
            ('/repo/dir2/subdir', (), ('final.md',)),
        ]
        
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/dir1', 'doc.md'),
            os.path.join('/repo/dir2', 'another.md'),
            os.path.join('/repo/dir2/subdir', 'final.md'),
        ]
        
        found_files = scavenger.find_markdown_files('/repo')
        self.assertCountEqual(found_files, expected_files)
        mock_walk.assert_called_once_with('/repo')

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_links(self, mock_file_open):
        # Mock rationale: Provide specific file content without reading from disk.
        mock_file_content = """
# My Document

This is a [link to example.com](https://example.com).
Another link: <http://anothersite.org/page>.
Internal link: [local doc](./docs/local.md).
Anchor link: [section](#section-header).
Broken internal: [non-existent](../nonexistent.md).
No link here.
"""
        mock_file_open.return_value.read.return_value = mock_file_content

        expected_links = [
            (4, 'https://example.com'),
            (5, 'http://anothersite.org/page'),
            (6, './docs/local.md'),
            (7, '#section-header'),
            (8, '../nonexistent.md'),
        ]
        
        extracted_links = scavenger.extract_links('dummy_path.md')
        self.assertCountEqual(extracted_links, expected_links)
        mock_file_open.assert_called_once_with('dummy_path.md', 'r', encoding='utf-8')

    @patch('requests.head')
    def test_check_external_link_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP response (status 200).
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        self.assertTrue(scavenger.check_external_link('https://example.com'))
        mock_head.assert_called_once_with('https://example.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_external_link_failure_404(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found HTTP response.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response
        
        self.assertFalse(scavenger.check_external_link('https://example.com/nonexistent'))

    @patch('requests.head')
    def test_check_external_link_failure_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error.
        mock_head.side_effect = scavenger.requests.exceptions.ConnectionError
        
        self.assertFalse(scavenger.check_external_link('https://badurl.com'))

    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join) # Use real os.path.join for path construction
    @patch('os.path.dirname', side_effect=os.path.dirname) # Use real os.path.dirname
    @patch('os.path.normpath', side_effect=os.path.normpath) # Use real os.path.normpath
    def test_check_internal_link_file_exists(self, mock_normpath, mock_dirname, mock_join, mock_exists):
        # Mock rationale: Simulate file existence without actual filesystem interaction.
        mock_exists.return_value = True
        
        base_path = '/repo/src/doc.md'
        target_path = '../assets/image.png'
        self.assertTrue(scavenger.check_internal_link(base_path, target_path))
        
        # Verify calls to os.path.exists with the correctly resolved path
        expected_full_path = os.path.normpath(os.path.join(os.path.dirname(base_path), target_path))
        mock_exists.assert_called_once_with(expected_full_path)

    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.path.dirname', side_effect=os.path.dirname)
    @patch('os.path.normpath', side_effect=os.path.normpath)
    def test_check_internal_link_file_does_not_exist(self, mock_normpath, mock_dirname, mock_join, mock_exists):
        # Mock rationale: Simulate a non-existent file.
        mock_exists.return_value = False
        
        base_path = '/repo/src/doc.md'
        target_path = '../assets/nonexistent.png'
        self.assertFalse(scavenger.check_internal_link(base_path, target_path))
        
        expected_full_path = os.path.normpath(os.path.join(os.path.dirname(base_path), target_path))
        mock_exists.assert_called_once_with(expected_full_path)

    @patch('os.path.exists')
    def test_check_internal_link_anchor_only(self, mock_exists):
        # Mock rationale: Anchor links within the same file are considered valid if the file exists.
        # We don't need to check os.path.exists for the anchor itself.
        base_path = '/repo/src/doc.md'
        target_path = '#section-header'
        self.assertTrue(scavenger.check_internal_link(base_path, target_path))
        mock_exists.assert_not_called() # Should not call exists for anchor-only links

    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.path.dirname', side_effect=os.path.dirname)
    @patch('os.path.normpath', side_effect=os.path.normpath)
    def test_check_internal_link_with_anchor_and_path_exists(self, mock_normpath, mock_dirname, mock_join, mock_exists):
        # Mock rationale: Simulate a file with an anchor that exists.
        mock_exists.return_value = True
        
        base_path = '/repo/src/doc.md'
        target_path = '../docs/another.md#subsection'
        self.assertTrue(scavenger.check_internal_link(base_path, target_path))
        
        expected_full_path = os.path.normpath(os.path.join(os.path.dirname(base_path), '../docs/another.md'))
        mock_exists.assert_called_once_with(expected_full_path)

    def test_is_external_url(self):
        self.assertTrue(scavenger.is_external_url('http://example.com'))
        self.assertTrue(scavenger.is_external_url('https://secure.org'))
        self.assertFalse(scavenger.is_external_url('./local.md'))
        self.assertFalse(scavenger.is_external_url('/absolute/path.md'))
        self.assertFalse(scavenger.is_external_url('#anchor'))

    @patch('scavenger.find_markdown_files')
    @patch('scavenger.extract_links')
    @patch('scavenger.check_external_link')
    @patch('scavenger.check_internal_link')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    def test_main_no_broken_links(self, mock_isdir, mock_exit, mock_print, mock_parse_args, 
                                   mock_check_internal, mock_check_external, mock_extract_links, 
                                   mock_find_markdown_files):
        # Mock rationale: Simulate a full run where all links are valid.
        mock_parse_args.return_value = MagicMock(repo='.')
        mock_find_markdown_files.return_value = ['/repo/README.md', '/repo/docs/guide.md']
        
        mock_extract_links.side_effect = [
            [(1, 'https://good-external.com'), (2, './docs/guide.md')], # README.md links
            [(1, 'https://another-good.com'), (2, '#section')],         # guide.md links
        ]
        
        mock_check_external.return_value = True
        mock_check_internal.return_value = True
        
        scavenger.main()
        
        mock_print.assert_any_call("\n✨ All links appear to be in order. The digital garden is well-tended.")
        mock_exit.assert_not_called() # Should not exit with error

    @patch('scavenger.find_markdown_files')
    @patch('scavenger.extract_links')
    @patch('scavenger.check_external_link')
    @patch('scavenger.check_internal_link')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    def test_main_with_broken_links(self, mock_isdir, mock_exit, mock_print, mock_parse_args, 
                                  mock_check_internal, mock_check_external, mock_extract_links, 
                                  mock_find_markdown_files):
        # Mock rationale: Simulate a full run where some links are broken.
        mock_parse_args.return_value = MagicMock(repo='.')
        mock_find_markdown_files.return_value = ['/repo/README.md']
        
        mock_extract_links.return_value = [
            (1, 'https://broken-external.com'),
            (2, './nonexistent.md'),
            (3, 'https://good-external.com'),
        ]
        
        # First external is broken, second internal is broken, third external is good
        mock_check_external.side_effect = [False, True] 
        mock_check_internal.return_value = False
        
        scavenger.main()
        
        mock_print.assert_any_call("🚨 BROKEN EXTERNAL LINK: /repo/README.md:1 -> https://broken-external.com")
        mock_print.assert_any_call("🚨 BROKEN INTERNAL LINK: /repo/README.md:2 -> ./nonexistent.md")
        mock_print.assert_any_call("\n⚠️ Some broken links were found. Time to get scavenging!")
        mock_exit.assert_called_once_with(1) # Should exit with error

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_repo_dir(self, mock_exit, mock_print, mock_parse_args, mock_isdir):
        # Mock rationale: Test the case where the provided repository directory does not exist.
        mock_parse_args.return_value = MagicMock(repo='/nonexistent/repo')
        
        scavenger.main()
        
        mock_print.assert_any_call("Error: Repository directory '/nonexistent/repo' not found.")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
