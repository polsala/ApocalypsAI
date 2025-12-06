import requests
import sys
from typing import List, Dict

def check_beacon(url: str, timeout: int = 5) -> Dict:
    """
    Checks the reachability of a single URL beacon.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if 200 <= response.status_code < 300:
            return {"url": url, "status": "UP", "status_code": response.status_code, "error": None}
        else:
            return {"url": url, "status": "DOWN", "status_code": response.status_code, "error": f"HTTP Error: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"url": url, "status": "DOWN", "status_code": None, "error": "Timeout"}
    except requests.exceptions.ConnectionError:
        return {"url": url, "status": "DOWN", "status_code": None, "error": "Connection Error"}
    except requests.exceptions.RequestException as e:
        return {"url": url, "status": "DOWN", "status_code": None, "error": f"Request Error: {e}"}

def main(urls: List[str]):
    """
    Main function to check a list of beacon URLs and print their status.
    """
    if not urls:
        print("No beacon URLs provided to check.")
        sys.exit(2) # No-op exit code

    results = []
    for url in urls:
        result = check_beacon(url)
        results.append(result)
        status_str = f"[{result['status']}] {result['url']}"
        if result['error']:
            status_str += f" ({result['error']})"
        elif result['status_code']:
            status_str += f" (HTTP {result['status_code']})"
        print(status_str)

    # Determine overall exit code
    if any(r["status"] == "DOWN" for r in results):
        sys.exit(1) # Failure if any beacon is down
    else:
        sys.exit(0) # Success if all beacons are up

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("Usage: python pinger.py <url1> [url2] ...")
        sys.exit(2)
