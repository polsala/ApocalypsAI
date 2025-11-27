import pytest
import os
from unittest.mock import patch, mock_open
from src.tracker import find_tangles, generate_report

# Mock rationale: os.walk is a file system traversal function.
# To make tests deterministic and offline, we must mock its behavior
# to simulate a specific directory structure and files without
# actually touching the disk.
@patch('os.walk')
# Mock rationale: open is used to read file contents.
# To make tests deterministic and offline, we must mock its behavior
# to return predefined content for specific file paths, avoiding
# actual file I/O.
@patch('builtins.open', new_callable=mock_open)
# Mock rationale: os.path.isfile is used to confirm a path points to a file.
# To ensure our mocked file paths are treated as valid files by the utility,
# we mock this to always return True for simplicity in these tests.
@patch('os.path.isfile', return_value=True)
def test_find_tangles_basic(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a directory structure with two files.
    # This allows testing file traversal and content reading without real disk access.
    mock_os_walk.return_value = [
        ('/project', ['src'], ['README.md']),
        ('/project/src', [], ['main.py', 'utils.py'])
    ]

    # Mock rationale: Define the content for each simulated file.
    # This ensures deterministic input for the `find_tangles` function.
    file_contents = {
        '/project/README.md': "This is a project.\nTODO: Update documentation.\n",
        '/project/src/main.py': "# Main script\n# FIXME: This needs refactoring.\ndef func(): pass\n",
        '/project/src/utils.py': "# Utility functions\n# HACK: Temporary solution.\n"
    }

    # Mock rationale: Configure mock_file_open to return specific content
    # when a file path is opened. This is crucial for offline testing of file reading.
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")

    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO', 'FIXME', 'HACK'])

    assert len(tangles) == 3
    assert '/project/README.md' in tangles
    assert tangles['/project/README.md'] == [('TODO', 2, 'Update documentation.')]
    assert '/project/src/main.py' in tangles
    assert tangles['/project/src/main.py'] == [('FIXME', 2, 'This needs refactoring.')]
    assert '/project/src/utils.py' in tangles
    assert tangles['/project/src/utils.py'] == [('HACK', 2, 'Temporary solution.')]

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.isfile', return_value=True)
def test_find_tangles_no_tangles(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a file system with files but no target keywords.
    # This verifies the function correctly handles cases with no matches.
    mock_os_walk.return_value = [
        ('/project', [], ['clean.py'])
    ]
    file_contents = {
        '/project/clean.py': "print('hello')\n# A regular comment.\n"
    }
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")
    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO'])
    assert len(tangles) == 0

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.isfile', return_value=True)
def test_find_tangles_multiple_in_one_file(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a file with multiple keywords to ensure all are captured.
    mock_os_walk.return_value = [
        ('/project', [], ['multi.py'])
    ]
    file_contents = {
        '/project/multi.py': "# TODO: First item\n# Another line\n# FIXME: Second item\n"
    }
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")
    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO', 'FIXME'])
    assert len(tangles) == 1
    assert '/project/multi.py' in tangles
    assert tangles['/project/multi.py'] == [
        ('TODO', 1, 'First item'),
        ('FIXME', 3, 'Second item')
    ]

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.isfile', return_value=True)
def test_find_tangles_case_insensitivity(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Test that keywords are matched regardless of case.
    mock_os_walk.return_value = [
        ('/project', [], ['case.py'])
    ]
    file_contents = {
        '/project/case.py': "# todo: lowercase\n# ToDo: mixed case\n"
    }
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")
    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO'])
    assert len(tangles) == 1
    assert tangles['/project/case.py'] == [
        ('TODO', 1, 'lowercase'),
        ('TODO', 2, 'mixed case')
    ]

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.isfile', return_value=True)
def test_find_tangles_exclude_dirs(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a directory structure including an excluded directory.
    # This tests the `exclude_dirs` functionality without real file system interaction.
    mock_os_walk.return_value = [
        ('/project', ['src', 'node_modules'], ['index.js']),
        ('/project/src', [], ['app.js']),
        ('/project/node_modules', [], ['dep.js'])
    ]
    file_contents = {
        '/project/index.js': "// TODO: Root file\n",
        '/project/src/app.js': "// TODO: App file\n",
        '/project/node_modules/dep.js': "// TODO: Dependency file\n"
    }
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")
    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO'], exclude_dirs=['node_modules'])
    assert len(tangles) == 2
    assert '/project/index.js' in tangles
    assert '/project/src/app.js' in tangles
    assert '/project/node_modules/dep.js' not in tangles # This file should be excluded

@patch('os.path.isdir', return_value=False) # Mock rationale: Simulate a non-existent directory.
def test_find_tangles_invalid_directory(mock_isdir):
    # Mock rationale: Test the error handling for an invalid input directory.
    with pytest.raises(ValueError, match="Directory not found"):
        find_tangles('/nonexistent', ['TODO'])

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.isfile', return_value=True)
def test_find_tangles_binary_file_skipped(mock_isfile, mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a binary file (.png) and a text file.
    # This ensures the utility skips non-text files gracefully.
    mock_os_walk.return_value = [
        ('/project', [], ['image.png', 'code.py'])
    ]
    file_contents = {
        '/project/code.py': "# TODO: This should be found\n",
        '/project/image.png': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'
    }

    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path == '/project/image.png':
            # For binary files, mock_open with read_data=bytes will cause a UnicodeDecodeError
            # if opened in text mode, which is what we want to test for graceful skipping.
            # Instead, we'll let the default mock_open handle it, and the errors='ignore'
            # in the actual code should prevent it from crashing.
            return mock_open(read_data=file_contents[file_path]).return_value
        elif file_path == '/project/code.py':
            return mock_open(read_data=file_contents[file_path]).return_value
        raise FileNotFoundError(f"No mock content for {file_path}")

    mock_file_open.side_effect = mock_open_side_effect

    tangles = find_tangles('/project', ['TODO'])
    assert len(tangles) == 1
    assert '/project/code.py' in tangles
    assert '/project/image.png' not in tangles

def test_generate_report_no_tangles():
    # Mock rationale: Test report generation when no tangles are found.
    report = generate_report({})
    assert "No Temporal Tangles Found!" in report
    assert "sparkling clean" in report

def test_generate_report_basic():
    # Mock rationale: Test basic report formatting with a few tangles.
    tangles = {
        '/project/src/main.py': [('FIXME', 2, 'This needs refactoring.')],
        '/project/README.md': [('TODO', 2, 'Update documentation.')]
    }
    report = generate_report(tangles, base_path='/project')
    assert "Temporal Tangle Report" in report
    assert "### File: `README.md`" in report
    assert "- Line 2: Update documentation." in report
    assert "### File: `src/main.py`" in report
    assert "- Line 2: This needs refactoring." in report
    assert "Generated by ApocalypsAI's Nightly Temporal Tangle Tracker 🤖" in report

def test_generate_report_multiple_in_file_and_keywords():
    # Mock rationale: Test report generation with multiple tangles in one file
    # and across different keywords, ensuring correct sorting.
    tangles = {
        '/project/app.py': [
            ('TODO', 5, 'Implement feature X'),
            ('FIXME', 10, 'Handle edge case Y'),
            ('TODO', 1, 'Initial setup')
        ]
    }
    report = generate_report(tangles, base_path='/project')
    assert "### File: `app.py`" in report
    assert "#### `FIXME`" in report
    assert "- Line 10: Handle edge case Y" in report
    assert "#### `TODO`" in report
    
    # Ensure sorting by line number within keyword, and keywords themselves
    # Keywords should be sorted alphabetically (FIXME before TODO)
    # Tangles within TODO should be sorted by line number (1 before 5)
    fixme_section_start = report.find("#### `FIXME`")
    todo_section_start = report.find("#### `TODO`")
    todo_line_1_index = report.find("- Line 1: Initial setup")
    todo_line_5_index = report.find("- Line 5: Implement feature X")
    fixme_line_10_index = report.find("- Line 10: Handle edge case Y")

    assert fixme_section_start != -1 and todo_section_start != -1
    assert fixme_section_start < todo_section_start # Keywords sorted alphabetically

    assert todo_line_1_index != -1 and todo_line_5_index != -1
    assert todo_line_1_index < todo_line_5_index # TODOs sorted by line number

    assert fixme_line_10_index != -1
