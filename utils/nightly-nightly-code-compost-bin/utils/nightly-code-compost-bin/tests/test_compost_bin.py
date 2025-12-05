import unittest
import os
from unittest.mock import patch, mock_open
import io
from src.compost_bin import find_compostable_code

class TestCompostBin(unittest.TestCase):

    # Mock rationale: os.walk is mocked to provide a deterministic file system
    # structure without actually touching the disk, ensuring tests are fast and isolated.
    @patch('os.walk')
    # Mock rationale: builtins.open is mocked to provide predefined file contents
    # as strings, avoiding actual file I/O and making tests deterministic.
    @patch('builtins.open', new_callable=mock_open)
    def test_no_compostable_code(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with a clean Python file.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['clean_code.py'])
        ]
        # Mock rationale: Provide the content for the 'clean_code.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """def func():
    print('hello')
# A single comment
pass
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_dead_code_if_false(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with a Python file containing 'if False:'.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['dead_code.py'])
        ]
        # Mock rationale: Provide the content for the 'dead_code.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """def func():
    if True:
        pass
    if False: # This should be flagged
        print('never runs')
    if 0:
        print('also never runs')
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['type'], 'Dead Code (if False/0:)')
        self.assertEqual(items[0]['line_number'], 4)
        self.assertEqual(items[1]['type'], 'Dead Code (if False/0:)')
        self.assertEqual(items[1]['line_number'], 6)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_consecutive_comments(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with a Python file containing a block of comments.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['comment_block.py'])
        ]
        # Mock rationale: Provide the content for the 'comment_block.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """# Header
# Another header line
# Yet another header line
def func():
    pass

# This is a comment
# This is another comment
# And a third one
# Fourth comment
"""
            )
        ]

        items = find_compostable_code('/tmp/project', min_consecutive_comments=3)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['type'], 'Consecutive Comments')
        self.assertEqual(items[0]['line_number'], '1-3')
        self.assertEqual(items[1]['type'], 'Consecutive Comments')
        self.assertEqual(items[1]['line_number'], '7-10')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_todo_fixme_markers(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with a Python file containing TODO/FIXME markers.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['markers.py'])
        ]
        # Mock rationale: Provide the content for the 'markers.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """def feature_a():
    # TODO: Implement this later
    pass

def feature_b():
    # FIXME: This logic is broken
    return 1
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['type'], 'TODO/FIXME Marker')
        self.assertEqual(items[0]['line_number'], 2)
        self.assertEqual(items[1]['type'], 'TODO/FIXME Marker')
        self.assertEqual(items[1]['line_number'], 6)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_ignore_directories(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a project structure with ignored directories.
        mock_os_walk.return_value = [
            ('/tmp/project', ['venv', 'src', 'build'], []), # Root dir
            ('/tmp/project/venv', [], ['script.py']), # Should be ignored
            ('/tmp/project/src', [], ['main.py']), # Should be scanned
            ('/tmp/project/build', [], ['output.py']) # Should be ignored
        ]
        # Mock rationale: Provide content for the 'main.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """# TODO: This should be found
def func(): pass
"""
            )
        ]

        items = find_compostable_code('/tmp/project', ignore_dirs=['venv', 'build'])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['file_path'], os.path.join('/tmp/project/src', 'main.py'))
        self.assertEqual(items[0]['type'], 'TODO/FIXME Marker')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_issues_in_one_file(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file with multiple types of compostable code.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['mixed_issues.py'])
        ]
        # Mock rationale: Provide content for the 'mixed_issues.py' file.
        mock_file_open.side_effect = [
            io.StringIO(
                """# First comment
# Second comment
# Third comment

def my_func():
    if False:
        print('dead')
    # TODO: Fix this later
    pass
"""
            )
        ]

        items = find_compostable_code('/tmp/project', min_consecutive_comments=3)
        self.assertEqual(len(items), 3)

        # Check for comment block
        self.assertEqual(items[0]['type'], 'Consecutive Comments')
        self.assertEqual(items[0]['line_number'], '1-3')

        # Check for dead code
        self.assertEqual(items[1]['type'], 'Dead Code (if False/0:)')
        self.assertEqual(items[1]['line_number'], 6)

        # Check for TODO
        self.assertEqual(items[2]['type'], 'TODO/FIXME Marker')
        self.assertEqual(items[2]['line_number'], 8)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_file(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an empty Python file.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['empty.py'])
        ]
        # Mock rationale: Provide empty content for the 'empty.py' file.
        mock_file_open.side_effect = [
            io.StringIO("")
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_only_comments_below_threshold(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file with comments, but not enough to trigger the consecutive comment rule.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['few_comments.py'])
        ]
        # Mock rationale: Provide content with only two consecutive comments.
        mock_file_open.side_effect = [
            io.StringIO(
                """# Comment 1
# Comment 2
def func(): pass
"""
            )
        ]

        items = find_compostable_code('/tmp/project', min_consecutive_comments=3)
        self.assertEqual(len(items), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_comments_interrupted(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file where comment blocks are interrupted by code.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['interrupted_comments.py'])
        ]
        # Mock rationale: Provide content where comments are broken by a line of code.
        mock_file_open.side_effect = [
            io.StringIO(
                """# Comment 1
# Comment 2
print('code')
# Comment 3
# Comment 4
# Comment 5
"""
            )
        ]

        items = find_compostable_code('/tmp/project', min_consecutive_comments=3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['type'], 'Consecutive Comments')
        self.assertEqual(items[0]['line_number'], '4-6')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_if_zero(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file with an 'if 0:' block.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['if_zero.py'])
        ]
        # Mock rationale: Provide content with an 'if 0:' block.
        mock_file_open.side_effect = [
            io.StringIO(
                """def test():
    if 0:
        print('this should be flagged')
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['type'], 'Dead Code (if False/0:)')
        self.assertEqual(items[0]['line_number'], 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_mixed_indentation_dead_code(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file with 'if False:' at different indentation levels.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['indentation.py'])
        ]
        # Mock rationale: Provide content with 'if False:' at various indents.
        mock_file_open.side_effect = [
            io.StringIO(
                """if False:
    pass
def func():
    if True:
        if False:
            pass
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['line_number'], 1)
        self.assertEqual(items[1]['line_number'], 5)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_todo_fixme_case_insensitivity(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file with TODO/FIXME markers in different cases.
        mock_os_walk.return_value = [
            ('/tmp/project', [], ['case_markers.py'])
        ]
        # Mock rationale: Provide content with various casing for markers.
        mock_file_open.side_effect = [
            io.StringIO(
                """# todo: lowercase
# FIXME: uppercase
# ToDo: mixed case
"""
            )
        ]

        items = find_compostable_code('/tmp/project')
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]['line_number'], 1)
        self.assertEqual(items[1]['line_number'], 2)
        self.assertEqual(items[2]['line_number'], 3)
