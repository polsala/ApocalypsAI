# Nightly Digital Dust Bunny

A high-performance CLI tool crafted in Rust to help you identify and sweep away "digital dust bunnies" – old, unused, or temporary files cluttering your file system. Keep your digital spaces tidy and efficient!

## Features

*   **Fast Traversal**: Leverages Rust's performance for quick directory scanning.
*   **Age-Based Filtering**: Easily specify how old a file must be to be considered a dust bunny.
*   **Dry Run Mode**: Preview which files would be deleted without making any changes.
*   **Safe Deletion**: Explicitly opt-in to delete files, preventing accidental data loss.
*   **Whimsical Output**: Adds a touch of fun to your system cleanup.

## Installation

To use `nightly-digital-dust-bunny`, you'll need [Rust](https://www.rust-lang.org/tools/install) installed.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny
    ```

2.  **Build the utility:**
    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `target/release/nightly-digital-dust-bunny`.** You can add it to your system's PATH for easier access.

## Usage

```bash
nightly-digital-dust-bunny [OPTIONS]
```

### Options

*   `-p, --path <PATH>`: Path to start sweeping for digital dust bunnies. Defaults to the current directory (`.`).
*   `-a, --age-days <DAYS>`: Files older than this many days will be considered dust bunnies. Defaults to `30` days.
*   `-d, --dry-run`: Perform a dry run without deleting any files. This is highly recommended for previewing.
*   `-D, --delete`: Delete the identified dust bunnies. **Use with extreme caution!** Cannot be used with `--dry-run`.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Find dust bunnies older than 60 days in your home directory (dry run):**
    ```bash
    nightly-digital-dust-bunny -p ~/ -a 60 --dry-run
    ```

2.  **Delete dust bunnies older than 7 days in a specific temporary folder:**
    ```bash
    nightly-digital-dust-bunny -p /tmp/my_temp_files -a 7 --delete
    ```

3.  **List all dust bunnies older than 30 days in the current directory (default behavior, dry run implied if --delete is not present):**
    ```bash
    nightly-digital-dust-bunny
    ```

## Development

### Running Tests

```bash
cargo test
```

### Project Structure

```
.gitignore
Cargo.toml
README.md
src/
└── main.rs
tests/
└── test_main.rs
```
