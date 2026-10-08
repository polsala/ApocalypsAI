# Nightly Void Scout

## Overview

The `nightly-void-scout` is a high-performance command-line utility designed to help you navigate the digital void of your file system. It allows you to quickly locate files and directories based on various criteria, such as name patterns (regex), size constraints, and modification timestamps. Think of it as an echo-locator for your digital artifacts, revealing their presence and properties.

## Features

*   **Pattern Matching**: Search for files and directories using regular expressions.
*   **Size Filtering**: Filter results by minimum and maximum file size.
*   **Time Filtering**: Locate items modified within a specified time frame (e.g., last 7 days, last 24 hours).
*   **Recursive Search**: Traverses directories recursively to find all matching 'echoes'.
*   **Human-Readable Output**: Displays file sizes in a user-friendly format.

## Installation

To install `nightly-void-scout`, you need to have Rust and Cargo installed. If you don't, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

1.  Clone the repository (or navigate to the `rust-utils/nightly-void-scout` directory if you have the full `ApocalypsAI` repo):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-void-scout
    ```
2.  Build and install the utility:
    ```bash
    cargo install --path .
    ```
    This will install `void-scout` to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
void-scout [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The root directory to start scouting from. Defaults to the current directory if not specified.

### Options

*   `-n, --name <REGEX>`: A regular expression to match against file and directory names. (e.g., `"\.log$"`, `"report.*\.txt"`)
*   `-s, --min-size <SIZE>`: Minimum file size (e.g., `100B`, `1KB`, `5MB`, `1GB`).
*   `-S, --max-size <SIZE>`: Maximum file size (e.g., `100B`, `1KB`, `5MB`, `1GB`).
*   `-m, --modified-since <DURATION>`: Only show items modified within the last duration (e.g., `7d`, `24h`, `30m`).
*   `-d, --directories-only`: Only show directories that match the criteria.
*   `-f, --files-only`: Only show files that match the criteria.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Find all `.log` files in the current directory and its subdirectories:**
    ```bash
    void-scout . --name "\.log$"
    ```

2.  **Find all files larger than 1MB modified in the last 3 days in your home directory:**
    ```bash
    void-scout ~/ --min-size 1MB --modified-since 3d
    ```

3.  **Locate directories named `cache` or `temp` anywhere under `/var`:**
    ```bash
    void-scout /var --name "^(cache|temp)$" --directories-only
    ```

4.  **Find files between 10KB and 100KB that contain 'report' in their name:**
    ```bash
    void-scout . --name "report" --min-size 10KB --max-size 100KB --files-only
    ```

## Development

To run tests:

```bash
cd rust-utils/nightly-void-scout
cargo test
```
