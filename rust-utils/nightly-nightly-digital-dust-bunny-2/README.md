# nightly-digital-dust-bunny

## Digital Dust Bunny Sweeper

This Rust CLI tool helps you identify and report on "digital dust bunnies" – files that are old, seemingly unused, or exact duplicates cluttering your file system. It's designed for performance and provides clear reports without modifying any files, giving you full control over what to keep or remove.

### Features

*   **Recursive Scanning**: Scans a specified directory and all its subdirectories.
*   **Age-based Reporting**: Identifies files that haven't been accessed or modified within a specified number of days. A special `--age 0` flag reports all files as 'old' for a comprehensive overview.
*   **Duplicate Detection**: Finds exact duplicate files using SHA256 content hashing, regardless of their names.
*   **Safe Operation**: Only reports findings; never deletes, moves, or modifies any files.
*   **High Performance**: Written in Rust for speed and efficiency, especially on large file systems.

### Installation

To install this utility, ensure you have Rust and Cargo installed. Then, navigate to the utility's directory and run:

```bash
cargo install --path .
```

This will compile the tool and make it available in your Cargo bin path (usually `~/.cargo/bin`).

### Usage

```bash
nightly-dust-bunny <PATH> [--age <DAYS>] [--duplicates]
```

**Arguments:**

*   `<PATH>`: The starting directory to scan. This is a required argument.

**Options:**

*   `--age <DAYS>`: Report files that have not been accessed or modified in the last `<DAYS>` days. If `0` is specified, all files will be reported as 'old'. (Default: `0`)
*   `--duplicates`: Enable detection and reporting of duplicate files based on their content hash.

### Examples

1.  **Find all files in the current directory and its subdirectories, reporting them as 'old' (using `--age 0`):**
    ```bash
    nightly-digital-dust-bunny . --age 0
    ```

2.  **Find files older than 365 days in your Downloads folder:**
    ```bash
    nightly-digital-dust-bunny ~/Downloads --age 365
    ```

3.  **Find duplicate files in your `/var/log` directory:**
    ```bash
    nightly-digital-dust-bunny /var/log --duplicates
    ```

4.  **Find files older than 90 days AND any duplicate files in your documents folder:**
    ```bash
    nightly-digital-dust-bunny ~/Documents --age 90 --duplicates
    ```

### Output

The tool will print messages to the console:

*   `[OLD]`: Indicates a file that matches the age criteria.
*   `Duplicate Files Found`: A section listing groups of identical files, showing their SHA256 hash and the paths to each duplicate.

Remember to review the output carefully before taking any action on the reported files.
