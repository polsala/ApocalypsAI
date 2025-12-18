A high-performance command-line utility written in Rust for calculating file hashes.

This tool supports multiple hashing algorithms and is designed for speed and efficiency.

## Usage

```bash
nightly-rust-file-hasher <algorithm> <file_path>
```

### Algorithms

Supported algorithms:

*   `md5`
*   `sha1`
*   `sha256`
*   `sha512`

### Examples

Calculate SHA256 hash of a file:

```bash
nightly-rust-file-hasher sha256 my_document.txt
```

Calculate MD5 hash of an image:

```bash
nightly-rust-file-hasher md5 my_photo.jpg
```

## Installation

(Instructions for building and installing the Rust binary would go here. For this example, we assume it's built and available in the PATH.)

## Development

This utility is built using Rust. To build it locally:

1.  Ensure you have Rust and Cargo installed.
2.  Clone this repository.
3.  Navigate to the `rust-utils/nightly-rust-file-hasher` directory.
4.  Run `cargo build --release`.
5.  The executable will be in `target/release/`.
