# Nightly Relic Rummager

`nightly-relic-rummager` is a whimsical-yet-useful command-line interface (CLI) tool built in Rust. It helps you sort through your digital hoard, identifying unique 'relics' (files) and flagging 'common junk' (duplicates) within a specified directory. It also provides a summary of file types found, helping you understand the composition of your scavenged data.

## Features

*   **High Performance**: Written in Rust for efficient file system traversal and SHA256 hashing.
*   **Duplicate Detection**: Identifies files with identical content, regardless of their name or location.
*   **File Type Summary**: Provides a breakdown of files by their extension.
*   **Recursive Scan**: Traverses subdirectories to ensure no relic is left unturned.
*   **Whimsical Output**: Presents findings with a touch of post-apocalyptic charm.

## Installation

To use `nightly-relic-rummager`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for installation instructions.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-relic-rummager
    ```

2.  **Build the project:**
    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `target/release/nightly-relic-rummager`.** You can add this path to your system's `PATH` environment variable for easier access, or run it directly.

## Usage

Run the tool by specifying the directory you wish to rummage through:

```bash
./target/release/nightly-relic-rummager <path_to_directory>
```

**Example:**

```bash
# Scan the current directory
./target/release/nightly-relic-rummager .

# Scan a specific directory
./target/release/nightly-relic-rummager /path/to/your/scavenged_data
```

### Arguments

*   `<path_to_directory>`: The path to the directory to scan. This argument is required.

## Output Example

```
Scanning for relics in: /path/to/your/scavenged_data

--- Rummaging Report ---

Total files scanned: 10
Total unique relics found: 7
Total common junk (duplicates): 3

--- Precious Artifacts (Unique Relics) ---

[SHA256: a1b2c3d4e5f6...] /path/to/your/scavenged_data/important_schematic.txt
[SHA256: b2c3d4e5f6a1...] /path/to/your/scavenged_data/old_log.log
[SHA256: c3d4e5f6a1b2...] /path/to/your/scavenged_data/notes/survival_tips.md
...

--- Common Junk (Duplicate Groups) ---

Hash: d4e5f6a1b2c3...
  - /path/to/your/scavenged_data/backup/old_photo.jpg
  - /path/to/your/scavenged_data/archive/old_photo_copy.jpg

Hash: e5f6a1b2c3d4...
  - /path/to/your/scavenged_data/temp/temp_file.txt
  - /path/to/your/scavenged_data/temp/another_temp_file.txt

--- File Type Manifest ---

.txt: 4 files
.jpg: 2 files
.log: 1 file
.md: 1 file
(No Extension): 2 files

--- End of Rummaging ---
May your unique finds be plentiful!
```
