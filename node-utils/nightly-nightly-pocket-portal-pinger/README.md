# Nightly Pocket Portal Pinger

## Overview

The `nightly-pocket-portal-pinger` is a whimsical-yet-useful command-line utility designed to help you monitor the "dimensional stability" of your critical digital and local "pocket portals." Whether it's a remote API endpoint, a web service, or a crucial local configuration file, this tool will ping them and report their status with a touch of apocalyptic charm.

It distinguishes between URLs (HTTP/HTTPS) and local file paths, providing appropriate status messages for each.

## Features

*   **URL Pinging**: Sends `HEAD` requests to specified URLs to check their availability and HTTP status codes.
*   **Local File Checking**: Verifies the existence and accessibility of local file paths.
*   **Whimsical Status Reports**: Translates standard statuses into "Dimensional Stability" reports:
    *   `Stable`: HTTP 200 OK or file exists.
    *   `Fluctuating`: HTTP 4xx client errors or file not found/inaccessible.
    *   `Collapsed`: HTTP 5xx server errors.
    *   `Unreachable`: Network errors for URLs.
*   **Batch Processing**: Reads a list of portals from a text file, allowing for easy monitoring of multiple resources.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-pocket-portal-pinger
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

To use the Pocket Portal Pinger, you need to provide a text file containing a list of portals, one per line. Each line can be either a full URL (starting with `http://` or `https://`) or a local file path.

**1. Create a portal list file (e.g., `portals.txt`)**:

```
https://api.example.com/status
http://legacy-service.internal
/etc/nginx/nginx.conf
./data/important_log.txt
https://another-api.com/health
```

**2. Run the pinger**:

```bash
node src/index.js portals.txt
```

**Example Output**:

```
Initiating Pocket Portal Pinger...
---------------------------------
[URL] https://api.example.com/status: Dimensional Stability: Stable (HTTP 200)
[URL] http://legacy-service.internal: Dimensional Stability: Fluctuating (HTTP 404)
[File] /etc/nginx/nginx.conf: Dimensional Stability: Stable
[File] ./data/important_log.txt: Dimensional Stability: Fluctuating (Error: File not found)
[URL] https://another-api.com/health: Dimensional Stability: Collapsed (HTTP 500)
---------------------------------
Pocket Portal Pinger complete.
```

## Development

### Running Tests

To ensure the dimensional integrity of the pinger itself, run the automated tests:

```bash
npm test
```

Tests are deterministic and offline, using mocks for file system and network operations.
