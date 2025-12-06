# Nightly Chrono-Scrub

A high-performance Rust CLI tool designed to help you identify and report on old, unused files that are "gathering digital dust" on your system. In the post-apocalyptic landscape of digital debris, `nightly-chrono-scrub` acts as your vigilant digital archaeologist, helping you pinpoint forgotten data fragments for potential archival or deletion, thus reclaiming precious storage and maintaining system hygiene.

## Features

*   **High Performance**: Built with Rust for speed and efficiency, ideal for scanning large directories.
*   **Age-Based Filtering**: Easily find files older than a specified duration (e.g., 90 days, 1 year).
*   **Size Filtering**: Filter files by minimum or maximum size.
*   **Exclusion Patterns**: Ignore files or directories matching specific patterns.
*   **Detailed Reporting**: Outputs file path, size, and last modification time for identified files.

## Installation

### Prerequisites

*   Rust toolchain (installable via `rustup`)

### Build from Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-scrub
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-chrono-scrub`. You can add it to your system's PATH for easy access.

## Usage

```bash
nightly-chrono-scrub --help
```

### Examples

1.  **Scan your home directory for files older than 90 days (default):**
    ```bash
    nightly-chrono-scrub -p ~/
    ```

2.  **Find files in `/var/log` older than 30 days:**
    ```bash
    nightly-chrono-scrub -p /var/log -a 30d
    ```

3.  **Identify files in a project directory older than 1 year, excluding `node_modules` and `.git` directories:**
    ```bash
    nightly-chrono-scrub -p ./my_project -a 1y -e node_modules -e .git
    ```

4.  **Find large files (over 100MB) in `/data` that haven't been touched in 6 months:**
    ```bash
    nightly-chrono-scrub -p /data -a 6m --min-size 100MB
    ```

5.  **Find small configuration files (under 1KB) in `/etc` older than 2 years:**
    ```bash
    nightly-chrono-scrub -p /etc -a 2y --max-size 1KB
    ```

## Development & Testing

To run the tests:

```bash
cargo test
```

The tests create temporary files and directories with specific modification times to ensure the utility correctly identifies and filters files based on age, size, and exclusion patterns.
