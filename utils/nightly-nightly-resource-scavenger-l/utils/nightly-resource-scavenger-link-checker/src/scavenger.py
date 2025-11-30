import requests
import sys
import os

def check_links(file_path: str) -> None:
    """
    Reads URLs from a file, checks their availability, and prints a summary.
    Exits with code 0 if all links are working, 1 otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: Link file '{file_path}' not found.")
        sys.exit(1)

    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

    if not urls:
        print(f"No URLs found in '{file_path}'. Nothing to scan.")
        sys.exit(0)

    print(f"Scanning {len(urls)} URLs...\n")

    results = []
    working_count = 0
    broken_count = 0

    for url in urls:
        try:
            # Use HEAD request for efficiency, as we only need the status code.
            # allow_redirects=True ensures we follow redirects to the final destination.
            response = requests.head(url, timeout=5, allow_redirects=True)
            status_code = response.status_code
            if 200 <= status_code < 400:
                print(f"[✅ {status_code}] {url}")
                results.append({'url': url, 'status': status_code, 'error': None})
                working_count += 1
            else:
                print(f"[❌ {status_code}] {url}")
                results.append({'url': url, 'status': status_code, 'error': f"HTTP Status {status_code}"})
                broken_count += 1
        except requests.exceptions.ConnectionError as e:
            print(f"[❌ ERR] {url} (ConnectionError: {e})")
            results.append({'url': url, 'status': None, 'error': f"ConnectionError: {e}"})
            broken_count += 1
        except requests.exceptions.Timeout:
            print(f"[❌ ERR] {url} (Timeout: Request timed out)")
            results.append({'url': url, 'status': None, 'error': "Timeout: Request timed out"})
            broken_count += 1
        except requests.exceptions.RequestException as e:
            print(f"[❌ ERR] {url} (RequestException: {e})")
            results.append({'url': url, 'status': None, 'error': f"RequestException: {e}"})
            broken_count += 1
        except Exception as e:
            # Catch any other unexpected errors
            print(f"[❌ ERR] {url} (Unexpected Error: {e})")
            results.append({'url': url, 'status': None, 'error': f"Unexpected Error: {e}"})
            broken_count += 1

    print("\n--- Scan Summary ---")
    print(f"Total URLs: {len(urls)}")
    print(f"Working URLs: {working_count}")
    print(f"Broken URLs: {broken_count}")

    if broken_count > 0:
        sys.exit(1) # Indicate failure if broken links are found
    else:
        sys.exit(0) # Indicate success


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/scavenger.py <link_file_path>")
        sys.exit(1)
    
    link_file = sys.argv[1]
    check_links(link_file)
