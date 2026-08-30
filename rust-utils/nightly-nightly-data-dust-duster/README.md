# Nightly Data Dust Duster

## Whimsical Utility: The Digital Dust Bunny Duster

In the post-apocalyptic digital wasteland, every byte of storage is precious, and every file holds potential secrets or vital information. But just like physical ruins, digital archives accumulate 'dust bunnies' – redundant, empty, or low-value files that clutter your precious data caches. The `nightly-data-dust-duster` is your high-performance Rust-powered broom, designed to sweep through your directories, identify these digital detritus, and help you reclaim valuable storage space.

### Features

*   **Empty File Detection**: Pinpoints files that take up space but contain no data.
*   **Duplicate File Identification**: Uses SHA256 hashing to find identical files, regardless of their name or location, ensuring you only keep one copy of critical data fragments.
*   **Recursive Scanning**: Traverses subdirectories to ensure no digital dust bunny hides unnoticed.
*   **Non-Recursive Option**: For when you only want to sweep the immediate vicinity.
*   **Fast & Efficient**: Built with Rust for blazing-fast file system traversal and hashing.

### Installation

To use the `nightly-data-dust-duster`, you'll need Rust and Cargo installed.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-data-dust-duster
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-data-dust-duster`.** You can move it to a directory in your system's PATH for easier access (e.g., `/usr/local/bin`).

### Usage

Run the `nightly-data-dust-duster` from your terminal. You must specify at least one detection option (`--empty` or `--duplicates`).

```bash
nightly-data-dust-duster [OPTIONS]
```

**Arguments:**

*   `-p, --path <PATH>`: The root directory to scan for dust bunnies. Defaults to the current directory (`.`).
*   `-e, --empty`: Report empty files (digital lint).
*   `-d, --duplicates`: Report duplicate files based on content hash (cloned critters).
*   `-n, --no-recursive`: Do not traverse subdirectories; only scan the specified path.

**Examples:**

1.  **Scan the current directory for empty files:**
    ```bash
    nightly-data-dust-duster --empty
    ```

2.  **Scan a specific archive directory for duplicate files:**
    ```bash
    nightly-data-dust-duster -p /path/to/your/archive --duplicates
    ```

3.  **Scan a project folder for both empty and duplicate files, but only in the top level:**
    ```bash
    nightly-data-dust-duster -p ~/my_project --empty --duplicates --no-recursive
    ```

4.  **Perform a full sweep for all digital dust bunnies in your data cache:**
    ```bash
    nightly-data-dust-duster -p /mnt/data_cache --empty --duplicates
    ```

### Contributing

Feel free to contribute to the `nightly-data-dust-duster` by suggesting new detection methods (e.g., low-entropy files, temporary file patterns) or performance enhancements. Every contribution helps keep the digital wasteland a little cleaner!
