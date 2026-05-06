# Nightly System Health Reporter

This utility is a whimsical bash script designed to report on the health of your system, framed with an apocalyptic flair. It gathers key system metrics and presents them in a fun, thematic way.

## Usage

Run the script from your terminal:

```bash
./nightly-sys-health-reporter.sh
```

## Features

*   **CPU Load**: Reports current CPU usage.
*   **Memory Usage**: Shows RAM and swap utilization.
*   **Disk Space**: Checks free space on mounted filesystems.
*   **Running Processes**: Lists the top N processes by CPU usage.
*   **Network Connections**: Displays active network connections.
*   **Apocalyptic Theming**: Presents the data with a touch of post-apocalyptic charm.

## Installation

1.  Clone the repository.
2.  Navigate to the `bash-utils/nightly-sys-health-reporter/src/` directory.
3.  Make the script executable:
    ```bash
    chmod +x nightly-sys-health-reporter.sh
    ```

## Testing

Automated tests are included to ensure the script functions correctly. Run them from the `bash-utils/nightly-sys-health-reporter/tests/` directory:

```bash
./test_nightly-sys-health-reporter.sh
```
