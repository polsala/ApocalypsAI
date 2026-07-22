# Nightly Reality Checksum (nrc)

`nrc` is a high-performance Rust CLI tool designed to help the community maintain the integrity of their digital assets against the unpredictable whims of temporal distortions and data corruption. It allows you to generate and verify cryptographic checksums for individual files or entire directory structures, ensuring that your data remains anchored in its intended reality.

## Features

*   **Fast & Reliable**: Built with Rust for maximum performance and memory safety.
*   **Recursive Checksumming**: Easily generate checksums for entire directories.
*   **Multiple Algorithms**: Supports SHA256 (default) and MD5 for flexibility.
*   **Verification**: Quickly check if files or directories have been altered since their last checksum generation.
*   **Whimsical Integrity**: Helps you sleep soundly, knowing your files haven't been swapped with alternate timeline versions.

## Installation

To install `nrc`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-reality-checksum
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-reality-checksum
cargo build --release
# The executable will be found at target/release/nrc
# You might want to add it to your PATH:
# cp target/release/nrc /usr/local/bin/
```

## Usage

### Generate Checksums

To generate checksums for a file or directory and save them to an output file:

```bash
nrc generate <path> -o <output_file.nrc>
```

**Examples:**

*   Generate SHA256 checksum for a single file:
    ```bash
nrc generate my_important_document.txt -o document.nrc
    ```

*   Generate SHA256 checksums for a directory recursively:
    ```bash
nrc generate my_project_folder/ -o project_checksums.nrc
    ```

*   Generate MD5 checksums for a directory:
    ```bash
nrc generate my_archive/ -o archive.md5.nrc --algorithm md5
    ```

### Verify Checksums

To verify files or directories against a previously generated checksum file:

```bash
nrc verify <path> -i <input_file.nrc>
```

**Examples:**

*   Verify a single file against its checksum:
    ```bash
nrc verify my_important_document.txt -i document.nrc
    ```

*   Verify a directory recursively against its checksums:
    ```bash
nrc verify my_project_folder/ -i project_checksums.nrc
    ```

### Command Line Options

```
nrc --help
```

```
nrc 0.1.0
A high-performance Rust CLI tool to generate and verify cryptographic checksums of files and directories.

USAGE:
    nrc <COMMAND>

COMMANDS:
    generate    Generate checksums for a file or directory
    verify      Verify files or directories against a checksum file
    help        Print this message or the help of the given subcommand(s)

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information
```

```
nrc generate --help
```

```
nrc-generate 0.1.0
Generate checksums for a file or directory

USAGE:
    nrc generate [OPTIONS] <PATH>

ARGS:
    <PATH>    Path to the file or directory to checksum

OPTIONS:
    -a, --algorithm <ALGORITHM>    Checksum algorithm to use (default: sha256) [possible values: sha256, md5]
    -h, --help                     Print help information
    -o, --output <OUTPUT>          Output file to write checksums to
```

```
nrc verify --help
```

```
nrc-verify 0.1.0
Verify files or directories against a checksum file

USAGE:
    nrc verify [OPTIONS] <PATH>

ARGS:
    <PATH>    Path to the file or directory to verify

OPTIONS:
    -h, --help                   Print help information
    -i, --input <INPUT>          Input checksum file to read from
    -s, --strict                 Fail if any file in the checksum file is missing from the path
```

## Checksum File Format

The output `.nrc` file uses a simple line-delimited format:

```
<algorithm>:<checksum_value>  <relative_filepath>
```

**Example:**

```
sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  ./empty.txt
sha256:2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e777  ./hello.txt
sha256:d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a6662eb4670d9  ./subdir/another.txt
```

Paths are always relative to the base path provided during generation or verification. This allows for flexible relocation of the checked directory.

## Contributing

Feel free to report issues or suggest improvements! This tool is part of the ApocalypsAI project, aiming to build robust utilities for a resilient future.
