import pytest
import os
from unittest.mock import patch, MagicMock
from collections import defaultdict

# Add the src directory to sys.path for importing auditor.py
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import audit_directory, format_size, print_report

# Mock rationale:
# We need to simulate a file system without actually creating files on disk.
# `os.walk` is mocked to return a predefined directory structure.
# `os.path.getsize` is mocked to return predefined file sizes.
# `os.path.isdir` is mocked to confirm the existence of the target directory.
# `sys.exit` is mocked to prevent the script from exiting during tests.
# `print` is mocked to capture output for assertion.

@pytest.fixture
def mock_filesystem():
    """Fixture to mock os.walk and os.path.getsize."""
    mock_walk_data = [
        ('/mock/archive', ['subdir1', 'subdir2'], ['file1.txt', 'image.jpg']),
        ('/mock/archive/subdir1', [], ['doc.pdf', 'data.json']),
        ('/mock/archive/subdir2', [], ['another.txt', 'noextfile']),
        ('/mock/archive/empty_dir', [], []),
    ]

    mock_file_sizes = {
        '/mock/archive/file1.txt': 1024,      # 1 KB
        '/mock/archive/image.jpg': 5 * 1024 * 1024, # 5 MB
        '/mock/archive/subdir1/doc.pdf': 2 * 1024 * 1024, # 2 MB
        '/mock/archive/subdir1/data.json': 512, # 0.5 KB
        '/mock/archive/subdir2/another.txt': 2048, # 2 KB
        '/mock/archive/subdir2/noextfile': 100, # 100 B
    }

    with patch('os.walk', return_value=mock_walk_data),
         patch('os.path.getsize', side_effect=lambda p: mock_file_sizes.get(p, 0)),
         patch('os.path.isdir', return_value=True):
        yield

def test_format_size():
    assert format_size(0) == "0 B"
    assert format_size(500) == "500 B"
    assert format_size(1024) == "1.0 KB"
    assert format_size(1536) == "1.5 KB"
    assert format_size(1024 * 1024) == "1.0 MB"
    assert format_size(1.5 * 1024 * 1024) == "1.5 MB"
    assert format_size(1024 * 1024 * 1024) == "1.0 GB"
    assert format_size(2.3 * 1024 * 1024 * 1024) == "2.3 GB"

def test_audit_directory_success(mock_filesystem):
    path = '/mock/archive'
    stats, total_files, total_size = audit_directory(path)

    expected_stats = defaultdict(lambda: {'count': 0, 'size': 0})
    expected_stats['.txt'] = {'count': 2, 'size': 1024 + 2048} # 1KB + 2KB
    expected_stats['.jpg'] = {'count': 1, 'size': 5 * 1024 * 1024} # 5MB
    expected_stats['.pdf'] = {'count': 1, 'size': 2 * 1024 * 1024} # 2MB
    expected_stats['.json'] = {'count': 1, 'size': 512} # 0.5KB
    expected_stats['(No Ext)'] = {'count': 1, 'size': 100} # 100B

    assert stats == expected_stats
    assert total_files == 6
    assert total_size == (1024 + 5*1024*1024 + 2*1024*1024 + 512 + 2048 + 100)

def test_audit_directory_empty(mock_filesystem):
    # mock_filesystem ensures os.path.isdir is True
    with patch('os.walk', return_value=[('/mock/empty_archive', [], [])]):
        path = '/mock/empty_archive'
        stats, total_files, total_size = audit_directory(path)
        assert not stats
        assert total_files == 0
        assert total_size == 0

def test_audit_directory_not_found():
    with patch('os.path.isdir', return_value=False),
         patch('sys.exit') as mock_exit,
         patch('builtins.print') as mock_print:
        audit_directory('/nonexistent/path')
        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_once_with("Error: Directory not found at '/nonexistent/path'", file=sys.stderr)

def test_print_report(mock_filesystem, capsys):
    path = '/mock/archive'
    stats, total_files, total_size = audit_directory(path)
    print_report(path, stats, total_files, total_size)
    captured = capsys.readouterr()

    output_lines = [line.strip() for line in captured.stdout.strip().split('\n')]

    # Check for presence of key lines, as exact order of extensions might vary slightly
    # though sorted() should make it deterministic.
    assert f"Apocalypse Archive Audit Report for: {path}" in output_lines
    assert "------------------------------------------------------------" in output_lines
    assert ".json    | Count:      1 | Size:   0.5 KB" in output_lines
    assert ".jpg     | Count:      1 | Size:   5.0 MB" in output_lines
    assert ".pdf     | Count:      1 | Size:   2.0 MB" in output_lines
    assert ".txt     | Count:      2 | Size:   3.0 KB" in output_lines
    assert "(No Ext) | Count:      1 | Size: 100 B" in output_lines
    assert "Total Files: 6" in output_lines
    assert "Total Size: 7.0 MB" in output_lines

def test_print_report_empty_directory(capsys):
    path = '/mock/empty_archive'
    stats = defaultdict(lambda: {'count': 0, 'size': 0})
    total_files = 0
    total_size = 0
    print_report(path, stats, total_files, total_size)
    captured = capsys.readouterr()

    expected_output = f"\nApocalypse Archive Audit Report for: {path}\n" \
                      + "-" * 60 + "\n" \
                      + "No files found in the specified directory.\n" \
                      + "-" * 60 + "\n"
    assert captured.stdout == expected_output
