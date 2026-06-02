# Nightly Temporal Data Lint Roller

A high-performance CLI tool crafted in Rust to help the community identify and clean up "temporal data lint" – files that are old, potentially unused, and cluttering your digital spaces. Think of it as a digital dust bunny collector for your filesystem, ensuring your data pathways remain clear and efficient.

## Features

*   **Age-based Lint Detection**: Easily find files older than a specified duration (e.g., 30 days, 1 week, 1 year).
*   **Dry Run Mode (Default)**: Safely preview which files would be affected before any deletion occurs.
*   **Deletion Mode**: Confidently remove identified lint with a dedicated flag.
*   **Recursive Scanning**: Traverses directories to find lint deep within your file structure.
*   **Whimsical yet Practical**: Keeps your digital environment tidy, preventing temporal data accumulation.

## Installation

To use the Nightly Temporal Data Lint Roller, you'll need Rust and Cargo installed. If you don't have them, you can install them via `rustup`: [https://rustup.rs/](https://rustup.rs/)

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    # If cloning the whole ApocalypsAI repo
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-data-lint-roller
    ```
    (Assuming this utility will be placed under `rust-utils/nightly-temporal-data-lint-roller`)

2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
    This will compile the executable and place it in `target/release/`.

## Usage

The utility operates from the command line.

```bash
# Navigate to the utility's directory if you haven't already
cd rust-utils/nightly-temporal-data-lint-roller
```

### Basic Dry Run (Default)

To see files older than 30 days in the current directory without deleting anything:

```bash
./target/release/nightly-temporal-data-lint-roller --age 30d
```

Or specify a different path:

```bash
./target/release/nightly-temporal-data-lint-roller --path /var/log --age 1y
```

### Deleting Temporal Lint

**WARNING**: Use the `--delete` flag with extreme caution. Files deleted are permanently removed. Always perform a dry run first!

To delete files older than 7 days in a specific directory:

```bash
./target/release/nightly-temporal-data-lint-roller --path ~/Downloads --age 7d --delete
```

### Age Duration Formats

The `--age` argument accepts the following formats:
*   `Xd`: X days (e.g., `30d`, `90d`)
*   `Xw`: X weeks (e.g., `1w`, `4w`)
*   `Xy`: X years (e.g., `1y`, `2y`)

### Full Options

```
nightly-temporal-data-lint-roller 0.1.0
A high-performance CLI tool to identify and clean up temporal data lint (old, unused files) across specified directories.

USAGE:
    nightly-temporal-data-lint-roller [OPTIONS] --age <AGE>

OPTIONS:
    -a, --age <AGE>      Files older than this duration will be considered lint. Examples: "30d", "1w", "1y"
    -d, --delete         Actually delete the identified temporal lint. Use with caution!
    -h, --help           Print help information
    -p, --path <PATH>    The directory to scan for temporal lint. [default: .]
    -r, --dry-run        Perform a dry run: list files that would be deleted without actually deleting them. This is
                         the default behavior.
    -V, --version        Print version information
```

## Development

### Running Tests

To run the automated tests:

```bash
cargo test
```

The tests create temporary files with specific modification times to ensure the utility correctly identifies and (optionally) deletes files based on the age criteria.
