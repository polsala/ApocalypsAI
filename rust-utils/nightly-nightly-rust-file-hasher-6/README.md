# nightly-rust-file-hasher

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool is a high-performance command-line interface (CLI) application built with Rust, designed to calculate cryptographic hashes of files. It supports multiple hashing algorithms for robust integrity verification.

## Philosophy

Inspired by the need for reliable data integrity checks in a chaotic world, this utility provides a fast and dependable way to ensure your files haven't been tampered with. Rust's performance and safety guarantees make it an ideal choice for this task.

## Installation

To install this utility, you'll need to have Rust and Cargo installed on your system. If you don't have them, you can install them from [rustup.rs](https://rustup.rs/).

1.  Clone this repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-rust-file-hasher
    ```

3.  Build the project:
    ```bash
    cargo build --release
    ```

    The executable will be located at `target/release/nightly-rust-file-hasher`.

## Usage

Run the utility from your terminal. The basic syntax is:

```bash
nightly-rust-file-hasher <algorithm> <file_path>
```

Replace `<algorithm>` with one of the supported hashing algorithms (e.g., `md5`, `sha1`, `sha256`, `sha512`) and `<file_path>` with the path to the file you want to hash.

### Supported Algorithms

*   `md5`
*   `sha1`
*   `sha256`
*   `sha512`

### Examples

Calculate the MD5 hash of a file named `important_document.txt`:

```bash
target/release/nightly-rust-file-hasher md5 important_document.txt
```

Calculate the SHA256 hash of an image file `apocalypse_logo.png`:

```bash
target/release/nightly-rust-file-hasher sha256 apocalypse_logo.png
```

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
