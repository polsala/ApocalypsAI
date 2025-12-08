# Nightly Temporal Drift Scrutinizer (`nightly-temporal-drift-scrut`)

A high-performance Rust CLI tool designed to detect "temporal data drifts" within your file system. In the chaotic aftermath, data can become fragmented, duplicated, or subtly altered across different locations. This utility helps you identify:

1.  **Exact Duplicates**: Files with identical content, regardless of their name or location.
2.  **Same Name, Different Content**: Files that share the same filename but have diverged in their content, indicating potential version conflicts or accidental modifications.

By pinpointing these drifts, the Scrutinizer helps maintain data integrity and reduce digital clutter, ensuring your critical information remains consistent and manageable.

## Features

*   **Recursive Scanning**: Traverses directories to find drifts deep within your file structure.
*   **SHA-256 Hashing**: Uses cryptographic hashing for reliable content comparison.
*   **Clear Reporting**: Presents detected drifts in an easy-to-read format.
*   **Performance**: Written in Rust for speed and efficiency on large datasets.

## Installation

To install `nightly-temporal-drift-scrut`, you need Rust and Cargo installed. If you don't have them, follow the instructions on [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install --path .
```

Alternatively, if you have the source:

```bash
git clone <repository-url>
cd nightly-temporal-drift-scrut
cargo build --release
# The executable will be in target/release/temporal-drift-scrut
```

## Usage

Run the `temporal-drift-scrut` command followed by the path to the directory you want to scan.

```bash
temporal-drift-scrut <path_to_directory>
```

### Examples

Scan the current directory:

```bash
temporal-drift-scrut .
```

Scan a specific directory:

```bash
temporal-drift-scrut /home/user/data_hoard
```

## Development & Testing

To run the tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License.
