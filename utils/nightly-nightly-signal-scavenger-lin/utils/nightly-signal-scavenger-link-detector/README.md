# Nightly Signal Scavenger Link Detector

## Overview

The `nightly-signal-scavenger-link-detector` is a whimsical-yet-useful utility designed to help maintain the integrity of your digital archives by scanning a list of URLs and reporting on their reachability. In the post-apocalyptic digital wasteland, ensuring your precious links still point to something meaningful is crucial. This tool acts as your signal scavenger, diligently checking for signs of life from distant servers.

It can read URLs from a specified file or directly from standard input, making it flexible for various integration scenarios. It provides a clear report indicating which links are reachable and which have succumbed to the digital decay.

## Usage

### Prerequisites

*   Python 3.11+
*   `requests` library (`pip install requests`)

### Running the Utility

1.  **From a file:**

    Create a text file (e.g., `urls.txt`) with one URL per line:

    ```
    https://www.google.com
    https://this-is-a-dead-link-example.com/404
    http://example.com/timeout-test
    ```

    Then run:

    ```bash
    python src/link_detector.py urls.txt
    ```

2.  **From standard input (stdin):**

    ```bash
    echo -e "https://www.github.com\nhttps://nonexistent-domain-12345.org" | python src/link_detector.py
    # Or manually type URLs and press Ctrl+D (Unix/Linux/macOS) or Ctrl+Z then Enter (Windows)
    ```

### Command-line Arguments

*   `<input_file>` (optional): Path to a file containing URLs, one per line. If omitted, URLs are read from stdin.
*   `--timeout <seconds>`: Sets the timeout for each URL request in seconds (default: `5.0`).

### Example Output

```
Checking 2 URLs with a timeout of 5.0 seconds...

--- Link Check Results ---
✅ REACHABLE | 200 | https://www.google.com (OK)
❌ UNREACHABLE | 404 | https://this-is-a-dead-link-example.com/404 (Client/Server Error)
```

### Exit Codes

*   `0`: All checked links are reachable (or no URLs were provided).
*   `1`: One or more unreachable links were detected.
