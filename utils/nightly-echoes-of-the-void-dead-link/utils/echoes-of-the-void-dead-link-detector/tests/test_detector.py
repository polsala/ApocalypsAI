import pytest
import sys
from unittest.mock import patch, mock_open
from io import StringIO
import requests

# Add the src directory to the path to allow importing detector.py
sys.path.insert(0, 'utils/echoes-of-the-void-dead-link-detector/src')
from detector import extract_urls, check_url, scan_files, main

# Mock rationale: We need to simulate network requests without actually making them
# to ensure tests are deterministic, fast, and offline. The `requests` library
# is external and relies on network access.
class MockResponse:
    def __init__(self, status_code, head_allowed=True):
        self.status_code = status_code
        self._head_allowed = head_allowed

    def raise_for_status(self):
        if self.status_code >= 400:
            # Create a mock response object for HTTPError to access status_code
            mock_error_response = MockResponse(self.status_code, self._head_allowed)
            raise requests.exceptions.HTTPError(response=mock_error_response)

    @property
    def request(self):
        # Mock request object for HTTPError to access method
        class MockRequest:
            method = 'HEAD' if self._head_allowed else 'GET'
        return MockRequest()

# Mock rationale: We need to simulate file system access without actually creating
# or reading files on disk. This makes tests deterministic and isolated.
@pytest.fixture
def mock_file_content():
    return {
        'file1.md': "This is a test file with a good link: https://example.com/good and a bad link: https://example.com/bad. Also a local link: /local/path.",
        'file2.txt': "Another file with just one link: https://example.com/another-good-one. And a duplicate: https://example.com/good",
        'empty.md': "No links here.",
        'no_links.txt': "Just plain text."
    }

@patch('requests.head')
@patch('requests.get')
def test_check_url_good_link(mock_get, mock_head):
    # Mock rationale: Simulate a successful HEAD request.
    mock_head.return_value = MockResponse(200)
    is_reachable, status_code = check_url("https://example.com/good")
    assert is_reachable is True
    assert status_code == 200
    mock_head.assert_called_once_with("https://example.com/good", timeout=5.0, allow_redirects=True)
    mock_get.assert_not_called()

@patch('requests.head')
@patch('requests.get')
def test_check_url_bad_link_404(mock_get, mock_head):
    # Mock rationale: Simulate a 404 Not Found HEAD request.
    mock_head.return_value = MockResponse(404)
    is_reachable, status_code = check_url("https://example.com/bad")
    assert is_reachable is False
    assert status_code == 404
    mock_head.assert_called_once()
    mock_get.assert_not_called()

@patch('requests.head')
@patch('requests.get')
def test_check_url_head_not_allowed_fallback_get_success(mock_get, mock_head):
    # Mock rationale: Simulate a server that doesn't allow HEAD (405) but allows GET (200).
    mock_head.return_value = MockResponse(405)
    mock_get.return_value = MockResponse(200)
    is_reachable, status_code = check_url("https://example.com/head-not-allowed")
    assert is_reachable is True
    assert status_code == 200
    mock_head.assert_called_once()
    mock_get.assert_called_once_with("https://example.com/head-not-allowed", timeout=5.0, allow_redirects=True, stream=True)

@patch('requests.head')
@patch('requests.get')
def test_check_url_head_not_allowed_fallback_get_fail(mock_get, mock_head):
    # Mock rationale: Simulate a server that doesn't allow HEAD (405) and GET fails (404).
    mock_head.return_value = MockResponse(405)
    mock_get.side_effect = requests.exceptions.HTTPError(response=MockResponse(404, head_allowed=False))
    is_reachable, status_code = check_url("https://example.com/head-not-allowed-get-fail")
    assert is_reachable is False
    assert status_code == 404
    mock_head.assert_called_once()
    mock_get.assert_called_once()

@patch('requests.head')
@patch('requests.get')
def test_check_url_connection_error(mock_get, mock_head):
    # Mock rationale: Simulate a network connection error.
    mock_head.side_effect = requests.exceptions.ConnectionError
    is_reachable, status_code = check_url("https://example.com/no-connection")
    assert is_reachable is False
    assert status_code == 0
    mock_head.assert_called_once()
    mock_get.assert_not_called()

@patch('requests.head')
@patch('requests.get')
def test_check_url_timeout(mock_get, mock_head):
    # Mock rationale: Simulate a request timeout.
    mock_head.side_effect = requests.exceptions.Timeout
    is_reachable, status_code = check_url("https://example.com/timeout")
    assert is_reachable is False
    assert status_code == 0
    mock_head.assert_called_once()
    mock_get.assert_not_called()

def test_extract_urls():
    content = "Visit our site at https://www.example.com/page. Also check http://anothersite.org/path?q=test and a markdown link [here](https://github.com/user/repo). No local links like /assets/image.png."
    urls = extract_urls(content)
    expected_urls = [
        "http://anothersite.org/path?q=test",
        "https://github.com/user/repo",
        "https://www.example.com/page"
    ]
    assert urls == sorted(expected_urls)

def test_extract_urls_no_links():
    content = "This is just plain text with no URLs."
    urls = extract_urls(content)
    assert urls == []

def test_extract_urls_duplicates():
    content = "Link 1: https://example.com/a. Link 2: https://example.com/b. Another Link 1: https://example.com/a."
    urls = extract_urls(content)
    expected_urls = [
        "https://example.com/a",
        "https://example.com/b"
    ]
    assert urls == sorted(expected_urls)

@patch('builtins.open', new_callable=mock_open)
@patch('requests.head')
@patch('requests.get')
def test_scan_files_all_good(mock_get, mock_head, mock_open_func, mock_file_content):
    # Mock rationale: Simulate all links being good.
    mock_open_func.side_effect = lambda f, *args, **kwargs: mock_open(read_data=mock_file_content[f]).return_value
    mock_head.return_value = MockResponse(200)

    results = scan_files(['file1.md', 'file2.txt'])
    assert not results
    # file1.md has 2 unique URLs, file2.txt has 1 unique URL (one is duplicate of file1.md good link)
    # So, 2 unique URLs from file1.md + 1 unique URL from file2.txt = 3 total unique URLs to check
    assert mock_head.call_count == 3
    assert mock_get.call_count == 0

@patch('builtins.open', new_callable=mock_open)
@patch('requests.head')
@patch('requests.get')
def test_scan_files_some_broken(mock_get, mock_head, mock_open_func, mock_file_content):
    # Mock rationale: Simulate some links being broken.
    mock_open_func.side_effect = lambda f, *args, **kwargs: mock_open(read_data=mock_file_content[f]).return_value

    def mock_head_side_effect(url, **kwargs):
        if "/bad" in url:
            return MockResponse(404)
        elif "/another-good-one" in url:
            return MockResponse(200)
        elif "/good" in url:
            return MockResponse(200)
        raise ValueError(f"Unexpected URL: {url}")

    mock_head.side_effect = mock_head_side_effect

    results = scan_files(['file1.md', 'file2.txt'])
    assert 'file1.md' in results
    assert len(results['file1.md']) == 1
    assert results['file1.md'][0] == ('https://example.com/bad', 404)
    assert 'file2.txt' not in results # Only good links in file2.txt
    assert mock_head.call_count == 3
    assert mock_get.call_count == 0

@patch('builtins.open', new_callable=mock_open)
@patch('requests.head')
@patch('requests.get')
def test_scan_files_file_not_found(mock_get, mock_head, mock_open_func, capsys):
    # Mock rationale: Simulate a file not being found on the filesystem.
    mock_open_func.side_effect = FileNotFoundError
    results = scan_files(['non_existent_file.md'])
    assert not results
    captured = capsys.readouterr()
    assert "Error: File not found: non_existent_file.md" in captured.stderr

@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
@patch('builtins.open', new_callable=mock_open)
@patch('requests.head')
@patch('requests.get')
def test_main_no_broken_links(mock_get, mock_head, mock_open_func, mock_stderr, mock_stdout, mock_file_content):
    # Mock rationale: Simulate a scenario where all links are good, and check main's exit code and output.
    mock_open_func.side_effect = lambda f, *args, **kwargs: mock_open(read_data=mock_file_content[f]).return_value
    mock_head.return_value = MockResponse(200)

    test_args = ['detector.py', 'file1.md']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 0
        output = mock_stdout.getvalue()
        assert "All links checked appear to be functional." in output

@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
@patch('builtins.open', new_callable=mock_open)
@patch('requests.head')
@patch('requests.get')
def test_main_with_broken_links(mock_get, mock_head, mock_open_func, mock_stderr, mock_stdout, mock_file_content):
    # Mock rationale: Simulate a scenario where some links are broken, and check main's exit code and output.
    mock_open_func.side_effect = lambda f, *args, **kwargs: mock_open(read_data=mock_file_content[f]).return_value

    def mock_head_side_effect(url, **kwargs):
        if "/bad" in url:
            return MockResponse(404)
        else:
            return MockResponse(200)

    mock_head.side_effect = mock_head_side_effect

    test_args = ['detector.py', 'file1.md']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 1
        output = mock_stdout.getvalue()
        assert "Detected broken links. Please investigate." in output
        assert "[BROKEN] https://example.com/bad (Status: 404)" in output
