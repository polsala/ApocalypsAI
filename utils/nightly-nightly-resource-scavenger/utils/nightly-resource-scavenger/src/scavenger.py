import argparse
import os
import re
import requests
from typing import List, Tuple, Dict, Any

# Regex to find URLs (http/https)
URL_REGEX = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

def find_urls_in_file(filepath: str) -> List[Tuple[str, int, str]]:
    """Finds all URLs in a given file and returns them with line numbers and line content."""
    urls_found = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for match in URL_REGEX.finditer(line):
                    urls_found.append((match.group(0), line_num, line.strip()))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return urls_found

def check_url(url: str) -> Tuple[int, str]:
    """Checks a single URL and returns its status code and reason."""
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400 and response.status_code not in [405]: # 405 Method Not Allowed, try GET
            return response.status_code, response.reason
        elif response.status_code == 405: # HEAD not allowed, try GET
            response = requests.get(url, timeout=5, allow_redirects=True, stream=True)
            response.close() # Close connection immediately after getting headers
            return response.status_code, response.reason
        return response.status_code, response.reason
    except requests.exceptions.ConnectionError:
        return 0, "Connection Error"
    except requests.exceptions.Timeout:
        return 0, "Timeout"
    except requests.exceptions.RequestException as e:
        return 0, str(e)

def main():
    parser = argparse.ArgumentParser(description="Scan files for broken URLs.")
    parser.add_argument('--path', type=str, default='.',
                        help='The root directory to start scanning from.')
    parser.add_argument('--extensions', nargs='+', default=['md', 'py'],
                        help='A space-separated list of file extensions to scan.')
    args = parser.parse_args()

    print(f"Scanning directory: {args.path}")
    print(f"Looking for files with extensions: {', '.join(args.extensions)}")

    all_urls_metadata: List[Dict[str, Any]] = []
    scanned_files_count = 0

    for root, _, files in os.walk(args.path):
        for file in files:
            if any(file.endswith(f'.{ext}') for ext in args.extensions):
                filepath = os.path.join(root, file)
                scanned_files_count += 1
                urls_in_file = find_urls_in_file(filepath)
                for url, line_num, line_content in urls_in_file:
                    all_urls_metadata.append({
                        'url': url,
                        'filepath': filepath,
                        'line_num': line_num,
                        'line_content': line_content
                    })
    
    print(f"Found {len(all_urls_metadata)} URLs in {scanned_files_count} files.")

    broken_links = []
    # Cache results for unique URLs to avoid re-checking the same URL multiple times
    checked_urls: Dict[str, Tuple[int, str]] = {}

    for url_info in all_urls_metadata:
        url = url_info['url']
        if url not in checked_urls:
            status_code, reason = check_url(url)
            checked_urls[url] = (status_code, reason)
        else:
            status_code, reason = checked_urls[url]

        if status_code >= 400 or status_code == 0: # 0 for connection errors/timeouts
            broken_links.append({
                'url': url,
                'filepath': url_info['filepath'],
                'line_num': url_info['line_num'],
                'status_code': status_code,
                'reason': reason
            })

    if broken_links:
        print("\nBroken Links:")
        print("--------------------------------------------------")
        for link in broken_links:
            status_str = f"[{link['status_code']} {link['reason'].upper()}]" if link['status_code'] != 0 else f"[ERROR: {link['reason']}]"
            print(f"{status_str} {link['url']} ({link['filepath']}:{link['line_num']})")
        print("--------------------------------------------------")
        print(f"Scan complete. {len(broken_links)} broken links found.")
        exit(1) # Exit with error code if broken links are found
    else:
        print("\nScan complete. No broken links found. All resources accounted for!")
        exit(0)

if __name__ == '__main__':
    main()
