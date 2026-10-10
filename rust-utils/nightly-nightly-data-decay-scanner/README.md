# Nightly Data Decay Scanner

`nightly-data-decay-scanner` is a whimsical-yet-useful command-line utility written in Rust that helps you identify 'digital detritus' in your filesystem. It scans a specified directory, calculates a 'decay score' for each file based on its last modification and access times, and then suggests whether the file is a candidate for archival or deletion.

Combat digital entropy and keep your data landscape tidy!

## Features

*   **Recursive Scanning**: Traverses directories to find all files.
*   **Decay Score Calculation**: Uses last modified and last accessed timestamps to determine how 'stale' a file is.
*   **Action Suggestions**: Categorizes files as 'Active Data', 'Archival Candidate', or 'Deletion Candidate' based on configurable thresholds.
*   **Performance**: Built with Rust for speed and efficiency in file system operations.

## Installation

To install `nightly-data-decay-scanner`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-data-decay-scanner
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-data-decay-scanner` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-data-decay-scanner <PATH> [OPTIONS]
```

### Arguments

*   `<PATH>`: The root directory to scan for data decay.

### Options

*   `-t, --threshold <DAYS>`: Sets the threshold in days for a file to be considered a 'Deletion Candidate'. Files older than `DAYS` will be marked for deletion. Files older than `DAYS / 2` (but not older than `DAYS`) will be marked for archival. Default is `365` days.
*   `-v, --verbose`: Show more detailed information, including exact decay days.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Scan the current directory with default thresholds:**
    ```bash
    nightly-data-decay-scanner .
    ```

2.  **Scan a specific directory with a custom deletion threshold of 180 days:**
    ```bash
    nightly-data-decay-scanner /path/to/my/old/projects -t 180
    ```

3.  **Scan with verbose output:**
    ```bash
    nightly-data-decay-scanner /var/log --verbose
    ```

## How Decay Score is Calculated

The decay score is primarily based on the maximum duration since the file was last modified or last accessed. The tool calculates `(current_time - max(last_modified_time, last_accessed_time))` and expresses this duration in days. A higher number of days indicates a higher decay score.

*   **Active Data**: `decay_days` < `threshold_days / 2`
*   **Archival Candidate**: `threshold_days / 2` <= `decay_days` < `threshold_days`
*   **Deletion Candidate**: `decay_days` >= `threshold_days`

*(Note: Last access time (`atime`) might not be reliably updated on all filesystems or configurations, especially for performance reasons. The tool will fall back to last modification time (`mtime`) if `atime` is unavailable or appears to be the epoch.)*
