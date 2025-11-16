# Nightly Signal-Scout Beacon Pinger

A whimsical-yet-useful command-line utility to monitor the reachability of critical "beacon" URLs. In a world of uncertain connectivity, this tool helps you keep tabs on your digital safe houses, essential services, or any web endpoint you need to ensure is still "UP."

## Features

*   **URL Reachability Check**: Attempts to connect to a list of provided URLs.
*   **Status Reporting**: Clearly indicates if a beacon is `UP` (HTTP 2xx) or `DOWN` (connection error, timeout, or other HTTP status).
*   **Error Details**: Provides specific error messages for `DOWN` beacons.
*   **CLI-driven**: Simple to use directly from your terminal or integrate into scripts.
*   **Self-contained**: No external configuration files needed beyond the command-line arguments.

## Installation

This utility is self-contained and written in Python 3.11. It requires the `requests` library.

1.  Navigate to the `utils/nightly-signal-scout-beacon-pinger/` directory.
2.  (Optional, but recommended) Create a Python virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install requests
    ```

## Usage

Run the `pinger.py` script with one or more URLs as arguments:

```bash
python src/pinger.py https://www.google.com https://www.github.com http://nonexistent.domain
```

### Example Output

```
[UP] https://www.google.com (HTTP 200)
[UP] https://www.github.com (HTTP 200)
[DOWN] http://nonexistent.domain (Connection Error)
```

### Exit Codes

The utility uses standard exit codes for scripting:

*   `0`: All specified beacons are `UP`.
*   `1`: One or more beacons are `DOWN`.
*   `2`: No URLs were provided as arguments (no-op).

## Development & Testing

To run the automated tests:

1.  Ensure dependencies are installed (see Installation).
2.  Navigate to the `utils/nightly-signal-scout-beacon-pinger/` directory.
3.  Run `unittest`:
    ```bash
    python -m unittest tests/test_pinger.py
    ```
