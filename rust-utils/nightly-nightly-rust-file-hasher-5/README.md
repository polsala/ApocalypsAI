# nightly-rust-file-hasher

A whimsical yet useful standalone utility for the community. This tool, built with Rust, provides a high-performance command-line interface for generating cryptographic hashes of files. It supports multiple common hashing algorithms.

## Philosophy

* **Speed and Efficiency**: Leverage Rust's performance characteristics for rapid file hashing.
* **Simplicity**: A straightforward CLI experience for everyday use.
* **Reliability**: Robust hashing algorithms for data integrity checks.

## Usage

```bash
# Install (assuming you have Rust and Cargo installed)
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main --path utils/nightly-rust-file-hasher

# Generate SHA-256 hash of a file
nightly-rust-file-hasher --algorithm sha256 --file path/to/your/file.txt

# Generate MD5 hash of a file
nightly-rust-file-hasher --algorithm md5 --file path/to/your/image.jpg

# List available algorithms
nightly-rust-file-hasher --list-algorithms
```

## Algorithms Supported

* md5
* sha1
* sha256
* sha512

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
