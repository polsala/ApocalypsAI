# Nightly Data Echo Collector

The "Nightly Data Echo Collector" is a whimsical-yet-useful utility designed to help you keep track of the digital whispers and echoes in your system. In a world where data can decay or proliferate unexpectedly, this tool acts as your vigilant scout, monitoring specified directories for file system changes (new, modified, or deleted files) and compiling a concise daily activity report.

It's perfect for tracking configuration changes, monitoring data drops, or simply understanding the ebb and flow of your digital wasteland.

## Features

*   **Directory Monitoring**: Recursively scans one or more specified directories.
*   **Change Detection**: Identifies new, modified, and deleted files since the last run.
*   **Concise Reporting**: Generates a human-readable report summarizing all detected changes.
*   **State Persistence**: Saves the file system state to a JSON file to enable comparison across runs.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js is supported.

## Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (if applicable) or navigate to the utility's directory**:
    ```bash
    cd nightly-data-echo-collector
    ```
3.  **Install dependencies**: This utility uses only built-in Node.js modules, so no `npm install` is strictly necessary for runtime, but `package.json` is provided for project context.

## Usage

The utility is run from the command line, requiring an output directory and one or more directories to monitor.

```bash
node src/main.js <output_directory> <directory_to_monitor_1> [directory_to_monitor_2 ...]
```

*   `<output_directory>`: The path where the `echo_state.json` (for state persistence) and `echo_report.txt` (the generated report) will be saved. This directory will be created if it doesn't exist.
*   `<directory_to_monitor_N>`: One or more paths to directories that the collector should scan for changes.

### Example

Let's say you want to monitor your `/var/log` and `/etc/config` directories, and save the reports and state in a `~/echo_reports` folder:

```bash
node src/main.js ~/echo_reports /var/log /etc/config
```

After the first run, `~/echo_reports/echo_state.json` will contain the initial state, and `~/echo_reports/echo_report.txt` will list all files as `[NEW]`.

On subsequent runs, the report will highlight only the changes that occurred since the last execution.

## Output

The `echo_report.txt` file will contain a summary similar to this:

```
--- Data Echo Report - 2023-10-27T10:30:00.000Z ---

[NEW] /var/log/syslog (Size: 12345 bytes)
[MODIFIED] /etc/config/nginx.conf (Old Size: 500, New Size: 550)
[DELETED] /var/log/old_app.log

--- Summary ---
New Files: 1
Modified Files: 1
Deleted Files: 1
-----------------
```

## Development and Testing

To run the automated tests:

```bash
npm test
```

The tests are deterministic and offline, using mocks for file system operations to ensure consistent results.
