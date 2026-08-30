# nightly-rust-file-hasher

A whimsical yet useful command-line utility built with Rust to efficiently compute cryptographic hashes of files. It supports MD5, SHA1, and SHA256 algorithms and offers flexible output formats (hexadecimal or base64).

## Features

*   **Blazing Fast**: Leverages Rust's performance for quick hashing.
*   **Multiple Algorithms**: Supports MD5, SHA1, and SHA256.
*   **Flexible Output**: Choose between hexadecimal (default) or Base64 encoding.
*   **Error Handling**: Gracefully handles file not found and other I/O errors.

## Installation

Ensure you have Rust and Cargo installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Build the utility:
    ```bash
    cargo build --release
    ```

3.  The executable will be located at `target/release/nightly-rust-file-hasher`.
    You can add this to your PATH for easier access.

## Usage

```bash
nightly-rust-file-hasher <file_path> [--algorithm <md5|sha1|sha256>] [--output <hex|base64>]
```

### Arguments

*   `<file_path>`: The path to the file you want to hash.

### Options

*   `--algorithm <md5|sha1|sha256>`: Specifies the hashing algorithm. Defaults to `sha256`.
*   `--output <hex|base64>`: Specifies the output encoding. Defaults to `hex`.

## Examples

*   Generate SHA256 hash (hexadecimal) of `my_document.txt`:
    ```bash
    target/release/nightly-rust-file-hasher my_document.txt
    ```

*   Generate MD5 hash (hexadecimal) of `important_data.bin`:
    ```bash
    target/release/nightly-rust-file-hasher important_data.bin --algorithm md5
    ```

*   Generate SHA1 hash in Base64 encoding of `config.yaml`:
    ```bash
    target/release/nightly-rust-file-hasher config.yaml --algorithm sha1 --output base64
    ```

## Testing

Run the tests using Cargo:

```bash
cargo test
```
