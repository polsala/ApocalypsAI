# Nightly Temporal Residue Scanner

## Summary
Scans directories for long-forgotten files, identifying them as 'temporal residue' for digital decluttering.

## Description
In the vast digital expanse, files often linger, unaccessed and unremembered, like faint echoes of past activity. These are what we call 'temporal residue'. The `nightly-temporal-residue-scanner` is a whimsical yet powerful Rust-based CLI tool designed to help you uncover these forgotten digital artifacts. By scanning specified directories, it identifies files that haven't been touched or modified within a given timeframe, presenting them as candidates for review, archiving, or deletion. It's your personal digital archaeologist, helping you declutter your storage and reclaim lost space.

## Features
*   **Recursive Scanning**: Traverses directories and their subdirectories to find all files.
*   **Age-Based Filtering**: Identifies files older than a specified number of days.
*   **Time Metric Choice**: Filter by last access time (`--access`) or last modification time (`--modified`, default).
*   **Whimsical Output**: Presents findings with a thematic flair, making decluttering a less daunting task.

## Installation
To install the `nightly-temporal-residue-scanner`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-temporal-residue-scanner
    ```
2.  Build and install the utility:
    ```bash
    cargo install --path .
    ```
    This will compile the binary and place it in your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage
Run the scanner from your terminal, specifying the path to scan and the age threshold.

```bash
nightly-temporal-residue-scanner <PATH> --age <DAYS> [--access | --modified]
```

### Arguments
*   `<PATH>`: The directory path to begin the scan. Use `.` for the current directory.
*   `--age <DAYS>`: (Optional) The minimum age in days for a file to be considered 'temporal residue'. Defaults to `365` days (1 year).
*   `--access`: (Optional) Use the file's last access time for age calculation. If neither `--access` nor `--modified` is specified, last modification time is used.
*   `--modified`: (Optional) Use the file's last modification time for age calculation. This is the default behavior.

### Examples

1.  **Scan the current directory for files older than 1 year (by modification time):**
    ```bash
    nightly-temporal-residue-scanner . --age 365
    ```

2.  **Scan a specific project folder for files not accessed in the last 6 months:**
    ```bash
    nightly-temporal-residue-scanner /home/user/old_projects --age 180 --access
    ```

3.  **Scan your entire home directory for files modified over 2 years ago:**
    ```bash
    nightly-temporal-residue-scanner /home/user --age 730 --modified
    ```

## Output
The scanner will print a whimsical message upon initiation, list any detected 'temporal residue' files with their last relevant timestamp, and conclude with a summary message.

```
🌌 Initiating Temporal Residue Scan in: /path/to/scan
⏳ Seeking echoes older than 365 days (modification time)...
--------------------------------------------------
👻 Found a faint echo: /path/to/scan/old_document.pdf (Last modified time: Tue, 01 Jan 2022 12:00:00 +0000)
👻 Found a faint echo: /path/to/scan/archive/forgotten_code.zip (Last modified time: Wed, 15 Feb 2021 09:30:00 +0000)
--------------------------------------------------
🧹 Temporal residue scan complete. Consider tidying these echoes of the past.
```

If no residue is found:

```
✨ No significant temporal residue detected. Your digital realm is pristine!
```
