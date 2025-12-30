# nightly-rust-file-hasher

A whimsical yet useful command-line utility written in Rust for calculating cryptographic hashes (MD5, SHA1, SHA256) of files. It's designed for speed and efficiency, with the potential for parallel processing on multi-core systems.

## Philosophy

"Speedy checksums for the discerning survivor." This tool aims to provide a robust and fast way to verify file integrity, a crucial task in any chaotic environment.

## Installation

Ensure you have Rust and Cargo installed.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main rust-utils/nightly-rust-file-hasher
```

## Usage

```bash
rust-file-hasher <FILE_PATH> [--algorithm <ALGORITHM>] [--threads <NUM_THREADS>]
```

*   `<FILE_PATH>`: The path to the file you want to hash.
*   `--algorithm <ALGORITHM>`: The hashing algorithm to use. Options are `md5`, `sha1`, `sha256` (default).
*   `--threads <NUM_THREADS>`: The number of threads to use for parallel processing. If not specified, the tool will use a sensible default based on your system's cores.

## Examples

Calculate SHA256 hash of a file:

```bash
rust-file-hasher my_important_document.txt
```

Calculate MD5 hash using 4 threads:

```bash
rust-file-hasher important_data.bin --algorithm md5 --threads 4
```

## Contributing

Contributions are welcome! Please follow the ApocalypsAI project guidelines.
