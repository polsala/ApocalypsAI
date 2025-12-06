# Nightly Signal Flare Sender

## Overview

The `nightly-signal-flare-sender` is a vital utility for navigating the digital wasteland. It scans a provided list of URLs, sending out 'signal flares' to determine if they are still alive and responsive. This helps identify dead links, broken resources, or unresponsive services, ensuring that your digital pathways remain clear and functional.

## Usage

To use the Signal Flare Sender, you need a plain text file where each line is a URL you wish to check.

```bash
python src/flare_sender.py --urls <path_to_your_url_file.txt>
```

**Example `urls.txt`:**

```
https://www.google.com
https://www.github.com/nonexistent-page
http://localhost:9999/unreachable
```

**Example Output:**

```
Initiating signal flare scan for 3 URLs...
Checking URL: https://www.google.com ... [200 OK]
Checking URL: https://www.github.com/nonexistent-page ... [404 Not Found]
Checking URL: http://localhost:9999/unreachable ... [Connection Error]
Signal flare scan complete.
```

## Installation

This utility requires the `requests` library. You can install it using pip:

```bash
pip install requests
```

## Development

To run tests:

```bash
python -m unittest tests/test_flare_sender.py
```
