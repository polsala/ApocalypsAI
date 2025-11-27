import pytest
import os
import builtins
from unittest.mock import patch, MagicMock
import requests.exceptions
import sys

from src.scavenger import (
    find_markdown_files,
    extract_links_from_markdown,
    check_link_status,
    main
)

# Mock rationale: os.walk is a file system operation. Mocking it allows
# us to simulate different directory structures without actual disk I/O,
# making tests deterministic and fast.
@patch('os.walk')
def test_find_markdown_files(mock_os_walk):
    # Simulate a directory structure
    mock_os_walk.return_value = [
        ('/test_dir', ['subdir'], ['file1.md', 'file2.txt']),
        ('/test_dir/subdir', [], ['file3.md', 'image.png'])
    ]
    
    files = find_markdown_files('/test_dir')
    assert sorted(files) == sorted([
        os.path.join('/test_dir', 'file1.md'),
        os.path.join('/test_dir', 'subdir', 'file3.md')
    ])

    mock_os_walk.return_value = []
    assert find_markdown_files('/empty_dir') == []

# Mock rationale: builtins.open is a file system operation. Mocking it allows
# us to provide specific file contents without creating actual files,
# ensuring tests are isolated and deterministic.
@patch('builtins.open', new_callable=MagicMock)
@patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
def test_extract_links_from_markdown(mock_os_path_exists, mock_open):
    # Test with various link formats
    mock_open.return_value.__enter__.return_value.read.return_value = """
# My README

This is a link to [Google](https://www.google.com).
Another link: https://example.org/path/to/resource.
A link with query params: [API Docs](https://api.example.com/v1?param=value&id=123).
No link here.
"""
    links = extract_links_from_markdown('/fake/path/README.md')
    expected_links = [
        "https://www.google.com",
        "https://example.org/path/to/resource",
        "https://api.example.com/v1?param=value&id=123"
    ]
    assert sorted(links) == sorted(expected_links)

    # Test with no links
    mock_open.return_value.__enter__.return_value.read.return_value = "No links in this file."
    assert extract_links_from_markdown('/fake/path/no_links.md') == []

    # Test with duplicate links
    mock_open.return_value.__enter__.return_value.read.return_value = """
[Link A](https://duplicate.com)
https://duplicate.com
"""
    links = extract_links_from_markdown('/fake/path/duplicates.md')
    assert links == ["https://duplicate.com"] # Should return unique links

# Mock rationale: requests.head and requests.get perform network requests.
# Mocking them prevents actual network calls, making tests fast, reliable,
# and independent of external service availability.
@patch('requests.head')
@patch('requests.get')
def test_check_link_status(mock_requests_get, mock_requests_head):
    # Test 200 OK (HEAD is sufficient)
    mock_requests_head.return_value.status_code = 200
    mock_requests_head.return_value.reason = "OK"
    status, reason = check_link_status("https://good.com")
    assert status == 200
    assert reason == "OK"
    mock_requests_head.assert_called_with("https://good.com", timeout=5)
    mock_requests_get.assert_not_called() # HEAD should be enough

    # Test 404 Not Found (HEAD is sufficient)
    mock_requests_head.return_value.status_code = 404
    mock_requests_head.return_value.reason = "Not Found"
    status, reason = check_link_status("https://broken.com")
    assert status == 404
    assert reason == "Not Found"

    # Test 500 Internal Server Error (HEAD is sufficient)
    mock_requests_head.return_value.status_code = 500
    mock_requests_head.return_value.reason = "Internal Server Error"
    status, reason = check_link_status("https://server-error.com")
    assert status == 500
    assert reason == "Internal Server Error"

    # Test 302 Redirect (HEAD returns 302, then GET is called)
    mock_requests_head.return_value.status_code = 302
    mock_requests_head.return_value.reason = "Found"
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.reason = "OK"
    status, reason = check_link_status("https://redirect.com")
    assert status == 200
    assert reason == "OK"
    mock_requests_head.assert_called_with("https://redirect.com", timeout=5)
    mock_requests_get.assert_called_with("https://redirect.com", timeout=5)

    # Test network error (e.g., ConnectionError)
    mock_requests_head.side_effect = requests.exceptions.ConnectionError("DNS lookup failed")
    status, reason = check_link_status("https://no-internet.com")
    assert status == 0
    assert "DNS lookup failed" in reason
    mock_requests_head.side_effect = None # Reset side effect for other tests

# Mock rationale: main function involves file system operations, network requests,
# and system exit. Mocking these allows us to test the end-to-end logic
# without actual side effects, controlling the test environment completely.
@patch('src.scavenger.find_markdown_files')
@patch('src.scavenger.extract_links_from_markdown')
@patch('src.scavenger.check_link_status')
@patch('argparse.ArgumentParser.parse_args')
@patch('builtins.print') # Mock rationale: Capture print output for assertion
@patch('sys.exit') # Mock rationale: Prevent actual program exit
def test_main_no_broken_links(mock_exit, mock_print, mock_parse_args, mock_check_link_status, mock_extract_links, mock_find_files):
    mock_parse_args.return_value.path = './test_dir'
    mock_find_files.return_value = ['/test_dir/README.md']
    mock_extract_links.return_value = ['https://good.com', 'https://another-good.com']
    mock_check_link_status.side_effect = [
        (200, "OK"),
        (200, "OK")
    ]

    main()

    mock_print.assert_any_call("No broken links found. All paths lead to glory!")
    mock_exit.assert_called_with(0) # Expect success exit code

@patch('src.scavenger.find_markdown_files')
@patch('src.scavenger.extract_links_from_markdown')
@patch('src.scavenger.check_link_status')
@patch('argparse.ArgumentParser.parse_args')
@patch('builtins.print')
@patch('sys.exit')
def test_main_with_broken_links(mock_exit, mock_print, mock_parse_args, mock_check_link_status, mock_extract_links, mock_find_files):
    mock_parse_args.return_value.path = './test_dir'
    mock_find_files.return_value = ['/test_dir/README.md', '/test_dir/docs/guide.md']
    
    # Simulate links for README.md
    mock_extract_links.side_effect = [
        ['https://good.com', 'https://broken.com', 'https://server-error.com'],
        ['https://another-broken.com']
    ]
    
    # Simulate status for links
    mock_check_link_status.side_effect = [
        (200, "OK"),
        (404, "Not Found"),
        (500, "Internal Server Error"),
        (0, "Connection refused") # Network error
    ]

    main()

    mock_print.assert_any_call("--- Broken Link Report ---\n")
    mock_print.assert_any_call("File: /test_dir/README.md")
    mock_print.assert_any_call("  - [Broken Link] https://broken.com (Status: 404 Not Found)")
    mock_print.assert_any_call("  - [Broken Link] https://server-error.com (Status: 500 Internal Server Error)")
    mock_print.assert_any_call("File: /test_dir/docs/guide.md")
    mock_print.assert_any_call("  - [Broken Link] https://another-broken.com (Status: Network Error: Connection refused)")
    mock_print.assert_any_call("Total broken links found: 3")
    mock_exit.assert_called_with(1) # Expect failure exit code

@patch('src.scavenger.find_markdown_files', return_value=[])
@patch('argparse.ArgumentParser.parse_args')
@patch('builtins.print')
@patch('sys.exit')
def test_main_no_markdown_files(mock_exit, mock_print, mock_parse_args, mock_find_files):
    mock_parse_args.return_value.path = './test_dir'
    
    main()

    mock_print.assert_any_call("Found 0 Markdown files.")
    mock_print.assert_any_call("No broken links found. All paths lead to glory!")
    mock_exit.assert_called_with(0)
