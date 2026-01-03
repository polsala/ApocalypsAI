# Nightly Syslog Filter Script (bash-utils)

This utility is a whimsical yet practical bash script designed to help you sift through the often overwhelming stream of syslog messages. It allows you to filter messages based on keywords and apply color coding for easier readability, making it a handy tool for system administrators and curious onlookers alike.

## Features

*   **Keyword Filtering**: Specify keywords to include or exclude messages.
*   **Color Coding**: Highlight important messages with distinct colors.
*   **Real-time Monitoring**: Can be used to tail log files in real-time.
*   **Customizable**: Easily modify keywords and colors.

## Usage

```bash
./nightly-syslog-filter-sh --include "error" --color-include "red" --exclude "debug" --color-exclude "blue" /var/log/syslog
```

### Arguments

*   `--include <keyword>`: Filter messages containing this keyword (case-insensitive).
*   `--color-include <color>`: Color for messages matching `--include` (e.g., `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`).
*   `--exclude <keyword>`: Filter messages containing this keyword (case-insensitive).
*   `--color-exclude <color>`: Color for messages matching `--exclude` (e.g., `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`).
*   `<log_file>`: The path to the syslog file to monitor.

**Note**: If no arguments are provided, the script will default to filtering for "error" in red and excluding "debug" in blue, and will attempt to read from `/var/log/syslog`.

## Installation

1.  Save the script as `nightly-syslog-filter-sh`.
2.  Make it executable: `chmod +x nightly-syslog-filter-sh`.

## Testing

Run the tests using the provided `test_nightly-syslog-filter-sh.sh` script.

```bash
./tests/test_nightly-syslog-filter-sh.sh
```
