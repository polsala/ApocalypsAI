## nightly-rust-file-hasher

A robust and lightning-fast command-line utility written in Rust for generating cryptographic hashes of files. It supports multiple common hashing algorithms and is designed for performance and reliability in the post-apocalyptic digital landscape.

### Usage

```bash
nightly-rust-file-hasher <algorithm> <file_path>
```

### Arguments

*   `<algorithm>`: The hashing algorithm to use. Supported algorithms:
    *   `md5`
    *   `sha1`
    *   `sha256`
    *   `sha512`

*   `<file_path>`: The path to the file you want to hash.

### Examples

Generate an MD5 hash of a critical data file:

```bash
nightly-rust-file-hasher md5 /data/critical_config.txt
```

Generate a SHA256 hash of a downloaded survival manual:

```bash
nightly-rust-file-hasher sha256 ./survival_manual_v3.pdf
```

### Installation

1.  Ensure you have Rust installed (`rustup`).
2.  Clone this repository.
3.  Navigate to the `utils/nightly-rust-file-hasher` directory.
4.  Build the project:
    ```bash
    cargo build --release
    ```
5.  The executable will be located at `target/release/nightly-rust-file-hasher`.
    You can copy this to your PATH for easier access.

### Contributing

This utility is part of the ApocalypsAI project. Contributions are welcome via pull requests.
