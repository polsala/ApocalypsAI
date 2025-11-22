import os
import re
import requests
import argparse
from typing import List, Tuple, Union

# Regex to find URLs in Markdown:
# 1. [link text](url) - captures the URL part
# 2. <url> - captures the URL inside angle brackets
URL_REGEX = re.compile(r'\[[^\]]+\]\((https?://[^)]+)\)|<(https?://[^>]+)>')

def extract_urls_from_markdown(content: str) -> List[str]:
    """Extracts URLs from Markdown content."""
    urls = []
    for match in URL_REGEX.finditer(content):
        if match.group(1):  # For [text](url) pattern
            urls.append(match.group(1))
        elif match.group(2): # For <url> pattern
            urls.append(match.group(2))
    return list(set(urls)) # Return unique URLs

def check_url(url: str, timeout: float = 5) -> Tuple[bool, Union[int, str]]:
    """Checks if a URL is accessible and returns its status or error."""
    try:
        # Use HEAD request for efficiency, as we only need the status code
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if 200 <= response.status_code < 400: # Success or redirect
            return True, response.status_code
        else:
            return False, response.status_code
    except requests.exceptions.ConnectionError:
        return False, "ConnectionError"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def scan_directory(path: str, exclude_patterns: List[str], timeout: float = 5) -> dict[str, List[Tuple[str, Union[int, str]]]]:
    """Scans a directory for Markdown files and checks their links."""
    broken_links_report: dict[str, List[Tuple[str, Union[int, str]]]] = {}

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prune directories based on exclude_patterns
        dirs[:] = [d for d in dirs if not any(p in d for p in exclude_patterns)]

        for file_name in files:
            if not file_name.endswith(('.md', '.markdown')):
                continue

            # Check if the file itself matches an exclude pattern
            if any(p in file_name for p in exclude_patterns):
                continue

            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, path)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                urls = extract_urls_from_markdown(content)

                file_broken_links = []
                for url in urls:
                    is_ok, status = check_url(url, timeout=timeout)
                    if not is_ok:
                        file_broken_links.append((url, status))
                
                if file_broken_links:
                    broken_links_report[relative_file_path] = file_broken_links

            except Exception as e:
                print(f"Error processing {relative_file_path}: {e}")

    return broken_links_report

def main():
    parser = argparse.ArgumentParser(description="Scan Markdown files for broken external links.")
    parser.add_argument('--path', type=str, default='.', help='The root directory to start scanning from.')
    parser.add_argument('--exclude-patterns', nargs='*', default=[], help='Space-separated list of directory/file name patterns to exclude.')
    parser.add_argument('--timeout', type=float, default=5.0, help='Timeout for HTTP requests in seconds.')

    args = parser.parse_args()

    print(f"Scanning for broken links in {args.path}...")
    report = scan_directory(args.path, args.exclude_patterns, args.timeout)

    if report:
        print("\nFound broken links:")
        for file_path, links in report.items():
            print(f"\nFile: {file_path}")
            for url, status in links:
                status_str = f"Status: {status}" if isinstance(status, int) else f"Error: {status}"
                print(f"  - {url} ({status_str})")
        exit(1) # Indicate failure for CI/CD
    else:
        print("\nNo broken links found. Repository documentation is healthy!")
        exit(0) # Indicate success

if __name__ == '__main__':
    main()
