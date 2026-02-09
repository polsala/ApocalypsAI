# Nightly Echo-Chamber Cleaner

## Whimsical Purpose
In the vast, echoing chambers of our digital existence, files often multiply, creating redundant 'echoes' that consume precious storage and mental clarity. The Nightly Echo-Chamber Cleaner is here to bring harmony to your directories, silencing these digital reverberations by identifying and managing duplicate files. Let's purify your data streams and ensure every byte sings a unique tune!

## Practical Utility
This is a high-performance command-line utility written in Rust that scans a specified directory for files with identical content. Once duplicates are found, it provides options to either safely delete the redundant copies (keeping one original) or replace them with hard links, saving disk space without losing file access.

## Features
*   **Duplicate Detection**: Uses SHA256 hashing for reliable content-based duplicate identification.
*   **Flexible Harmonization**: Choose between deleting duplicates or replacing them with hard links.
*   **Dry Run Mode**: Preview changes before committing to any file system modifications.
*   **Performance**: Built with Rust for speed and efficiency, especially on large directories.

## Installation

### Prerequisites
*   Rust toolchain (rustup recommended)

### Build from Source
1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-echo-chamber-cleaner
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `./target/release/echo-chamber-cleaner`.
    Consider adding it to your system's PATH for easier access:
    ```bash
    sudo cp ./target/release/echo-chamber-cleaner /usr/local/bin/
    ```

## Usage
```bash
nightly-echo-chamber-cleaner <DIRECTORY> [OPTIONS]
```

### Arguments
*   `<DIRECTORY>`: The path to the directory to scan for duplicate files.

### Options
*   `-a, --action <ACTION>`: Specify the action to take on duplicates. 
    *   `delete`: Delete all but one instance of each duplicate group. (Default)
    *   `link`: Replace all but one instance of each duplicate group with hard links to the original file.
*   `-d, --dry-run`: Perform a dry run, printing what actions would be taken without modifying the file system.
*   `-v, --verbose`: Enable verbose output.
*   `-h, --help`: Print help information.

### Examples

1.  **Find and delete duplicates (dry run):**
    ```bash
    nightly-echo-chamber-cleaner ~/my_documents --dry-run
    ```

2.  **Find and delete duplicates (actual run):**
    ```bash
    nightly-echo-chamber-cleaner ~/my_documents --action delete
    ```

3.  **Find and replace duplicates with hard links:**
    ```bash
    nightly-echo-chamber-cleaner /var/log/archives --action link
    ```

4.  **Verbose dry run:**
    ```bash
    nightly-echo-chamber-cleaner ./my_photos --dry-run --verbose
    ```

## How it Works
1.  The tool traverses the specified directory, identifying all regular files.
2.  For each file, it computes a SHA256 hash of its content.
3.  Files with identical hashes are grouped as duplicates.
4.  Based on the chosen action (`delete` or `link`):
    *   **Delete**: One instance of the file is kept, and all other duplicates are removed.
    *   **Link**: One instance is kept, and all other duplicates are replaced with hard links pointing to the kept file. This saves disk space as hard links share the same inode and data blocks.

## Contributing
Feel free to contribute to the harmonization effort! Open issues or pull requests on the main ApocalypsAI repository.
