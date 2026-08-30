# nightly-rust-file-hasher

A whimsical yet useful standalone utility built with Rust. This command-line tool allows users to generate and verify file checksums using a variety of cryptographic hash functions, all with blazing-fast performance.

## Philosophy

Inspired by the need for robust integrity checks in a chaotic digital world, this tool provides a reliable and efficient way to ensure your files haven't been tampered with or corrupted. Rust's performance characteristics make it ideal for this task.

## Features

*   **Multiple Hashing Algorithms**: Supports SHA-256, SHA-512, MD5, and Blake3.
*   **Fast Performance**: Leverages Rust's speed for quick hashing operations.
*   **Verification Mode**: Compares a file's calculated checksum against a provided reference.
*   **Standalone Binary**: Easy to distribute and use.

## Installation

Ensure you have Rust and Cargo installed.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main --path rust-utils/nightly-rust-file-hasher
```

Alternatively, you can clone the repository and build it locally:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-rust-file-hasher
cargo build --release
```

The executable will be in `target/release/`.

## Usage

**Generate Checksum:**

```bash
nightly-rust-file-hasher <file_path> [--algorithm <sha256|sha512|md5|blake3>]
```

*   `file_path`: The path to the file you want to hash.
*   `--algorithm`: (Optional) The hashing algorithm to use. Defaults to `sha256`.

**Example:**

```bash
nightly-rust-file-hasher my_important_document.txt
nightly-rust-file-hasher my_secret_data.bin --algorithm blake3
```

**Verify Checksum:**

```bash
nightly-rust-file-hasher verify <file_path> <expected_checksum> [--algorithm <sha256|sha512|md5|blake3>]
```

*   `file_path`: The path to the file to verify.
*   `expected_checksum`: The known checksum of the file.
*   `--algorithm`: (Optional) The hashing algorithm used to generate the `expected_checksum`. Defaults to `sha256`.

**Example:**

```bash
nightly-rust-file-hasher verify my_important_document.txt abc123def456...
```

## Testing

Unit tests are included and can be run using Cargo:

```bash
cd rust-utils/nightly-rust-file-hasher
cargo test
```
