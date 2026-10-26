# Nightly Temporal Echo Sync

`nightly-temporal-echo-sync` is a high-performance Rust CLI tool designed to detect and report file system changes by comparing the current state of a directory against a previously captured 'temporal echo' snapshot.

This utility is invaluable for:
-   **Configuration Drift Detection**: Ensure critical configuration files haven't been unexpectedly altered.
-   **Integrity Checks**: Verify that important data files remain untampered.
-   **Change Tracking**: Monitor directories for new, modified, or deleted files over time.
-   **Whimsical Temporal Stability**: Keep your digital timelines aligned and free from 'temporal distortions'.

## Features

-   **Snapshot Creation**: Generate a `.echo_snapshot.json` file containing SHA256 hashes and sizes of all files in a specified directory.
-   **Change Comparison**: Compare the current directory state against a snapshot, reporting `NEW`, `MODIFIED`, and `DELETED` files.
-   **Recursive Scanning**: Efficiently traverses subdirectories.
-   **Fast & Reliable**: Built with Rust for speed and memory safety.

## Installation

To install `nightly-temporal-echo-sync`, you need to have Rust and Cargo installed. If you don't have them, you can get them from [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-echo-sync
    ```

2.  **Build and install using Cargo:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-temporal-echo-sync` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

The utility provides two main commands: `snapshot` and `compare`.

### 1. Create a Temporal Echo Snapshot

Use the `snapshot` command to capture the current state of a directory. This will generate a JSON file (by default, `.echo_snapshot.json`) containing metadata for all files.

```bash
nightly-temporal-echo-sync snapshot <directory_path> [OPTIONS]
```

**Arguments:**
-   `<directory_path>`: The path to the directory you want to snapshot.

**Options:**
-   `-o, --output <FILE>`: Specify the output file path for the snapshot. Defaults to `.echo_snapshot.json` in the current directory.

**Example:**

```bash
# Create a snapshot of your current project directory
nightly-temporal-echo-sync snapshot .

# Create a snapshot of a specific configuration directory, saving to a custom file
nightly-temporal-echo-sync snapshot /etc/nginx -o /var/lib/echo_snapshots/nginx_config.json
```

### 2. Compare Against a Temporal Echo Snapshot

Use the `compare` command to check for any 'temporal distortions' (changes) in a directory relative to a saved snapshot.

```bash
nightly-temporal-echo-sync compare <directory_path> [OPTIONS]
```

**Arguments:**
-   `<directory_path>`: The path to the directory you want to compare.

**Options:**
-   `-i, --input <FILE>`: Specify the input snapshot file path. Defaults to `.echo_snapshot.json` in the current directory.

**Example:**

```bash
# Compare your current project directory against its default snapshot
nightly-temporal-echo-sync compare .

# Compare a configuration directory against a specific snapshot file
nightly-temporal-echo-sync compare /etc/nginx -i /var/lib/echo_snapshots/nginx_config.json
```

**Output:**

If no changes are detected:
```
No temporal distortions detected. All files are in sync with the echo.
```

If changes are detected:
```
Temporal distortions detected!
NEW: "new_file.txt"
MODIFIED: "config/app.conf"
DELETED: "old_log.txt"
```

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
