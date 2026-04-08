# nightly-rust-file-hasher

A whimsical yet useful command-line utility written in Rust to efficiently compute various cryptographic hashes for files. It supports MD5, SHA1, SHA256, and SHA512, and can optionally leverage multiple CPU cores for faster processing of large files.

## Philosophy

Inspired by the need for robust integrity checks in a post-apocalyptic world where data corruption could be catastrophic, this tool provides a fast and reliable way to verify file integrity. Rust's performance and safety guarantees make it ideal for such a critical task.

## Installation

1. **Prerequisites**: Ensure you have Rust and Cargo installed. If not, follow the official Rust installation guide: [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

2. **Build from source**: Clone this repository and navigate to the utility's directory:
   ```bash
   git clone https://github.com/polsala/ApocalypsAI.git
   cd ApocalypsAI/rust-utils/nightly-rust-file-hasher
   cargo build --release
   ```

3. **Executable**: The compiled binary will be located at `target/release/nightly-rust-file-hasher`.

## Usage

```bash
nightly-rust-file-hasher <FILE_PATH> [OPTIONS]
```

### Arguments

*   `<FILE_PATH>`: The path to the file for which to compute hashes.

### Options

*   `-a, --algorithm <ALGORITHM>`: Specify the hashing algorithm to use. Supported algorithms are `md5`, `sha1`, `sha256`, `sha512`. Defaults to `sha256`.
*   `-p, --parallel`: Enable parallel processing for potentially faster hashing of large files. This uses multiple threads.
*   `-h, --help`: Display help message.

### Examples

*   Compute SHA256 hash of a file:
    ```bash
    ./target/release/nightly-rust-file-hasher my_important_document.txt
    ```

*   Compute MD5 hash of a file:
    ```bash
    ./target/release/nightly-rust-file-hasher my_config.json -a md5
    ```

*   Compute SHA512 hash in parallel:
    ```bash
    ./target/release/nightly-rust-file-hasher large_data_archive.tar.gz -a sha512 -p
    ```

## Testing

Automated tests are included to ensure the utility functions correctly. You can run them using Cargo:

```bash
cd rust-utils/nightly-rust-file-hasher
cargo test
```

## Contributing

This is an autonomous agent-generated utility. Contributions are welcome via pull requests, adhering to the ApocalypsAI project's philosophy of "Anarchy with discipline."
