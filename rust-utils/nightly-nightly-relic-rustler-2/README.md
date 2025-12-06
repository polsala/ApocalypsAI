# Nightly Relic Rustler

A high-performance CLI tool crafted in Rust to help survivors manage their most precious digital 'relics' in the post-apocalyptic landscape. It allows you to compute SHA256 checksums for integrity, whimsically scramble files with a 'temporal frequency' key for obfuscation, unscramble them, and verify their original content.

## Features

*   **Checksum**: Generate SHA256 hashes of any file to ensure its integrity against cosmic rays or digital decay.
*   **Scramble**: Apply a simple XOR-based 'temporal distortion field' to your files using a secret 'temporal frequency' key, making them unreadable to casual observers.
*   **Unscramble**: Reverse the temporal distortion, restoring your files to their original state with the correct key.
*   **Verify**: Confirm that a scrambled file, once unscrambled with the provided key, matches a known original SHA256 hash, ensuring your relics are truly preserved.

## Installation

To use the Relic Rustler, you'll need Rust and Cargo installed. If you don't have them, follow the instructions on [rust-lang.org](https://www.rust-lang.org/tools/install).

1.  **Clone the repository (or navigate to the utility's directory):**

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-relic-rustler
    ```

2.  **Build the utility:**

    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `./target/release/nightly-relic-rustler`.** You can add it to your system's PATH for easier access, or run it directly.

    ```bash
    # Example: Add to PATH (temporary for current session)
    export PATH="$(pwd)/target/release:$PATH"
    ```

## Usage

All commands are accessed via `nightly-relic-rustler <command> [options]`.

### 1. Checksum a file

Computes the SHA256 hash of a given file.

```bash
nightly-relic-rustler checksum --file path/to/your/relic.txt
# Example Output:
# SHA256 of path/to/your/relic.txt: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0f37fa42af0
```

### 2. Scramble a file

Obfuscates a file using a simple XOR cipher with your chosen 'temporal frequency' key.

```bash
nightly-relic-rustler scramble --input path/to/original.txt --output path/to/scrambled.bin --key "whispers_of_the_void"
# Example Output:
# File 'path/to/original.txt' scrambled to 'path/to/scrambled.bin' with key.
```

### 3. Unscramble a file

Restores a scrambled file to its original content using the same 'temporal frequency' key.

```bash
nightly-relic-rustler unscramble --input path/to/scrambled.bin --output path/to/restored.txt --key "whispers_of_the_void"
# Example Output:
# File 'path/to/scrambled.bin' unscrambled to 'path/to/restored.txt' with key.
```

### 4. Verify a scrambled file

Checks if a scrambled file, when unscrambled with the provided key, matches a known original SHA256 hash.

```bash
# First, get the original hash
nightly-relic-rustler checksum --file path/to/original.txt
# Let's say the hash is: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0f37fa42af0

# Then, verify the scrambled file
nightly-relic-rustler verify --scrambled-file path/to/scrambled.bin --original-hash d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0f37fa42af0 --key "whispers_of_the_void"
# Example Output (Success):
# Verification successful! Original content hash matches.

# Example Output (Failure):
# Verification FAILED! Expected hash: ..., Actual hash: ...
```

## Development & Testing

To run the tests for this utility:

```bash
cd rust-utils/nightly-relic-rustler
cargo test
```

Tests use `tempfile` to create temporary files for I/O operations, ensuring they are deterministic and do not interfere with your filesystem.
