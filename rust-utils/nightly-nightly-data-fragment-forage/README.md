# Nightly Data Fragment Forager

In the post-apocalyptic digital wasteland, data can become fragmented, duplicated, or simply forgotten. The `nightly-data-fragment-forager` is your trusty companion, a high-performance CLI tool designed to sift through the digital debris and identify files that are empty, duplicated by content, or have become ancient relics of a bygone era.

Keep your data streams clean and your storage optimized, even when the world around you is in chaos!

## Features

*   **Digital Voids Detection**: Quickly finds empty files that consume space without purpose.
*   **Echoes in the Data Stream**: Identifies duplicate files by content hashing, revealing redundant copies.
*   **Ancient Relics Discovery**: Flags files older than a specified number of days, helping you unearth forgotten data or identify candidates for archival/deletion.
*   **High Performance**: Built with Rust for speed and memory efficiency, ideal for scanning large file systems.

## Installation

To install `nightly-data-fragment-forager`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

```bash
cargo install nightly-data-fragment-forager
```

This will compile and install the `data-fragment-forager` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

## Usage

Run the `data-fragment-forager` command followed by one or more paths to scan and the desired detection flags.

```bash
data-fragment-forager <PATH>... [OPTIONS]
```

### Arguments

*   `<PATH>...`: One or more paths (directories or files) to scan. Directories will be traversed recursively.

### Options

*   `--duplicates`: Detect duplicate files by comparing their SHA256 content hashes.
*   `--empty`: Detect files that have zero bytes.
*   `--ancient <DAYS>`: Detect files that were last modified more than `<DAYS>` ago.
*   `--help`: Print help information.
*   `--version`: Print version information.

## Examples

1.  **Scan a directory for empty files:**

    ```bash
    data-fragment-forager /path/to/my/data --empty
    ```

2.  **Find duplicate files in multiple locations:**

    ```bash
    data-fragment-forager /home/user/documents /mnt/backup --duplicates
    ```

3.  **Identify files older than 90 days in your archives:**

    ```bash
    data-fragment-forager /var/log /opt/old_projects --ancient 90
    ```

4.  **Perform a comprehensive scan for all types of debris:**

    ```bash
    data-fragment-forager . --empty --duplicates --ancient 365
    ```

## Output

The tool will print categorized reports for each type of digital debris found. If no debris is detected for the specified checks, a reassuring message will be displayed.
