# nightly-rust-file-hasher

A whimsical yet useful command-line utility written in Rust for generating cryptographic hashes of files. It's designed for speed and reliability, perfect for ensuring the integrity of your precious post-apocalyptic data caches.

## Features

*   Supports multiple hashing algorithms: MD5, SHA-1, SHA-256, SHA-512.
*   Blazing fast performance thanks to Rust's efficiency.
*   Simple and intuitive command-line interface.
*   Handles large files gracefully.

## Installation

Ensure you have Rust and Cargo installed. Then, clone this repository and build the utility:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI
cargo build --release
```

The executable will be located at `target/release/nightly-rust-file-hasher`.

## Usage

```bash
./target/release/nightly-rust-file-hasher <algorithm> <file_path>
```

### Arguments

*   `<algorithm>`: The hashing algorithm to use. Supported options are `md5`, `sha1`, `sha256`, `sha512`.
*   `<file_path>`: The path to the file you want to hash.

### Examples

Generate an MD5 hash for a file named `survival_guide.txt`:

```bash
./target/release/nightly-rust-file-hasher md5 survival_guide.txt
```

Generate a SHA-256 hash for a critical data backup file:

```bash
./target/release/nightly-rust-file-hasher sha256 data_backup_v3.tar.gz
```

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
