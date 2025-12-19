# Nightly Chrono-Scrub

In the post-apocalyptic digital wasteland, file timestamps can be... unreliable. System clocks drift, data gets corrupted, and sometimes, files just seem to exist out of time. The `nightly-chrono-scrub` is your trusty Rust-powered temporal anomaly detector, designed to scan your file system for these chronological distortions.

It helps you identify:
*   **Stale Files**: Files that haven't been modified in an unusually long time, potentially forgotten backups or lingering debris.
*   **Future-Dated Files**: Files whose modification or creation times are set in the future, indicating a system clock issue, malicious tampering, or a temporal paradox.
*   **Inconsistent Timestamps**: Files where the modification time precedes the creation time, a clear sign of data corruption or manipulation.

Keep your digital archives tidy and free from temporal paradoxes!

## Features

*   **High Performance**: Written in Rust for blazing-fast directory traversal and metadata processing.
*   **Stale File Detection**: Configurable threshold for identifying old, untouched files.
*   **Future-Dated File Detection**: Flags files with timestamps ahead of the current system time, with an adjustable tolerance for clock skew.
*   **Inconsistent Timestamp Detection**: Pinpoints files where modification time is earlier than creation time.
*   **Verbose Output**: Get detailed information about each detected anomaly.

## Installation

Make sure you have Rust and Cargo installed. If not, visit [rustup.rs](https://rustup.rs/).

1.  Navigate to the `rust-utils/nightly-chrono-scrub` directory.
2.  Build and install the utility:
    ```bash
    cargo install --path .
    ```

This will install `chrono-scrub` to your Cargo bin directory, usually `~/.cargo/bin`, and make it available in your PATH.

## Usage

```bash
chrono-scrub [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The root directory to start scanning from. Defaults to the current directory if not specified.

### Options

*   `--stale-days <DAYS>`: Detects files not modified in at least `DAYS` days. (e.g., `--stale-days 365` for files older than a year).
*   `--future-tolerance <SECONDS>`: Detects files with creation/modification times more than `SECONDS` into the future. Defaults to `60` seconds to account for minor clock skew.
*   `--inconsistent`: Detects files where the modification time is earlier than the creation time.
*   `--verbose`, `-v`: Enable verbose output, showing more details for each anomaly.
*   `--help`, `-h`: Print help information.
*   `--version`, `-V`: Print version information.

## Examples

1.  **Scan the current directory for any anomalies (stale, future, inconsistent) with default future tolerance:**
    ```bash
    chrono-scrub .
    ```

2.  **Find files older than 90 days in your documents folder:**
    ```bash
    chrono-scrub /home/user/documents --stale-days 90
    ```

3.  **Identify future-dated files with a 5-minute (300 seconds) tolerance in your backups:**
    ```bash
    chrono-scrub /mnt/backups --future-tolerance 300
    ```

4.  **Check for inconsistent timestamps across your entire home directory, with verbose output:**
    ```bash
    chrono-scrub /home/user --inconsistent -v
    ```

5.  **Combine all checks for a comprehensive temporal audit:**
    ```bash
    chrono-scrub /var/log --stale-days 180 --future-tolerance 120 --inconsistent
    ```

## Contributing

Feel free to report issues or suggest improvements! May your timestamps be ever consistent.
