# Nightly Chrono-Scrub

## Temporal Detritus Management for the Discerning Survivor

In the ever-shifting sands of the digital wasteland, files accumulate like forgotten memories, slowing down your systems and cluttering your precious storage. The `nightly-chrono-scrub` is your trusty companion, a high-performance Rust CLI tool designed to meticulously scan your directories for 'temporal detritus' – files that are either ancient and untouched, or insidious duplicates lurking in the shadows.

Think of it as a digital archaeologist, sifting through the ruins of your file system to unearth what truly matters and what can be safely recycled into the void.

## Features

*   **Age-Based Cleanup**: Identify files that haven't been accessed or modified in a specified number of days.
*   **Duplicate Detection**: Find identical files across your scanned paths using robust content hashing.
*   **Dry Run Mode**: Preview all identified detritus before any permanent action is taken (default behavior).
*   **Interactive Deletion**: Safely remove identified files with an explicit `--delete` flag and confirmation prompt.
*   **Recursive Scanning**: Traverse entire directory trees to ensure no digital dust bunny is missed.

## Installation

To install `nightly-chrono-scrub`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

1.  Clone the repository (or navigate to the `nightly-chrono-scrub` directory if you've downloaded it):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-scrub
    ```
2.  Build and install the utility:
    ```bash
    cargo install --path .
    ```
    This will make the `chrono-scrub` command available in your shell.

## Usage

`chrono-scrub` operates on a specified path and can be configured with various options.

```bash
chrono-scrub --help
```

```
A high-performance CLI tool to identify and clean up old, unused, or duplicate files across specified directories, treating them as 'temporal detritus'.

Usage: chrono-scrub [OPTIONS] --path <PATH>

Options:
  -p, --path <PATH>        The root directory to scan for temporal detritus
  -a, --age <DAYS>         Identify files not accessed or modified in the last N days
  -d, --duplicates         Identify duplicate files by content hash
  -s, --min-size <BYTES>   Minimum file size (in bytes) to consider for age/duplicate checks [default: 1]
  -v, --verbose            Enable verbose output
      --delete             Actually delete the identified files (requires confirmation)
      --dry-run            Perform a dry run, showing what would be deleted without actual deletion (default)
  -h, --help               Print help
  -V, --version            Print version
```

### Examples

1.  **Dry run: Find files older than 90 days in your 'archive' directory:**
    ```bash
    chrono-scrub --path /path/to/your/archive --age 90
    ```
    This will list all files that haven't been accessed or modified in the last 90 days, without deleting them.

2.  **Dry run: Find duplicate files in your 'data_dumps' directory:**
    ```bash
    chrono-scrub --path /path/to/your/data_dumps --duplicates
    ```
    This will list groups of identical files, showing their paths and content hash.

3.  **Dry run: Combine age and duplicate detection in your 'temp_zone' directory:**
    ```bash
    chrono-scrub --path /path/to/your/temp_zone --age 30 --duplicates
    ```
    This will list files older than 30 days AND any duplicate files found.

4.  **Actual deletion: Remove files older than 180 days in 'old_logs' (with confirmation):**
    ```bash
    chrono-scrub --path /path/to/old_logs --age 180 --delete
    ```
    **WARNING**: This will prompt you for confirmation before deleting files. Use with caution!

5.  **Actual deletion: Remove duplicate files larger than 1KB in 'staging_area':**
    ```bash
    chrono-scrub --path /path/to/staging_area --duplicates --min-size 1024 --delete
    ```

## Development

To run the tests, navigate to the utility's directory and use Cargo:

```bash
cd rust-utils/nightly-chrono-scrub
cargo test
```
