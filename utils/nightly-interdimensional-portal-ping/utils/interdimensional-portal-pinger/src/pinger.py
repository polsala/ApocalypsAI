import requests
import sys
import os

PORTALS_FILE = 'portals.txt'
DEFAULT_TIMEOUT = 5 # seconds

def read_portals(filepath):
    """Reads a list of portal URLs from a file."""
    if not os.path.exists(filepath):
        print(f"Error: Portal file '{filepath}' not found. Please create it with one URL/IP per line.", file=sys.stderr)
        return []
    try:
        with open(filepath, 'r') as f:
            portals = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return portals
    except IOError as e:
        print(f"Error reading portal file '{filepath}': {e}", file=sys.stderr)
        return []

def ping_portal(url):
    """Attempts to ping a single portal (URL) and returns its status."""
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return f"ONLINE (Status: {response.status_code})"
        else:
            return f"ONLINE (Status: {response.status_code}) - Non-200"
    except requests.exceptions.ConnectionError:
        return "OFFLINE (Connection Error)"
    except requests.exceptions.Timeout:
        return "UNKNOWN_ERROR (Request Timeout)"
    except requests.exceptions.RequestException as e:
        return f"UNKNOWN_ERROR ({type(e).__name__})"
    except Exception as e:
        # Catch any other unexpected errors during the request
        return f"CRITICAL_ERROR ({type(e).__name__})"

def main():
    print("🌌 Initiating Interdimensional Portal Ping... 🌌\n")

    # Determine the directory of the current script to find portals.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    portals_filepath = os.path.join(script_dir, PORTALS_FILE)

    portals = read_portals(portals_filepath)

    if not portals:
        print("No portals found to ping. Exiting.")
        return

    for portal_url in portals:
        status = ping_portal(portal_url)
        print(f"[{portal_url}] - {status}")

    print("\n🌌 Interdimensional Scan Complete. 🌌")

if __name__ == '__main__':
    main()
