# Nightly Temporal Echo Finder

## Summary

The `nightly-temporal-echo-finder` is a high-performance command-line utility crafted in Rust to help the community detect "temporal echoes" – our whimsical term for duplicate files. By comparing cryptographic hashes (SHA-256) of file contents, this tool efficiently identifies files that are identical, regardless of their names or locations. It's an essential utility for tidying up digital archives and ensuring data integrity in the post-apocalyptic landscape.

## Features

*   **Blazing Fast:** Leverages Rust's performance for rapid file traversal and hashing.
*   **Content-Based Detection:** Identifies duplicates based on file content, not just name or size.
*   **Recursive Scanning:** Scans directories and all their subdirectories.
*   **Clear Output:** Presents detected echoes in an easy-to-read format.

## Installation

To install `nightly-temporal-echo-finder`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

Navigate to the utility's directory and use Cargo:

```bash
cd rust-utils/nightly-temporal-echo-finder
cargo install --path .
```

Alternatively, if you have the source code:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-echo-finder
cargo build --release
# The executable will be found at target/release/nightly-temporal-echo-finder
```

## Usage

Run the utility by providing one or more paths to directories you wish to scan for temporal echoes.

```bash
nightly-temporal-echo-finder <PATH1> [PATH2] ...
```

**Example:**

```bash
nightly-temporal-echo-finder ./my_documents /var/log/archive
```

### Output Format

The tool will group identical files together, indicating their shared "temporal resonance" (hash) and listing all paths that share that resonance.

```
Temporal Echoes Detected! Initiating Resonance Scan...

--- Echo Group 1 ---
Resonance Field (SHA256): a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /path/to/file1.txt
  - /path/to/backup/file1_copy.txt

--- Echo Group 2 ---
Resonance Field (SHA256): f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9
  - /path/to/image.jpg
  - /path/to/archive/old_image.jpg

Resonance scan complete. Temporal echoes identified.
```

If no echoes are found:

```
Temporal Echoes Detected! Initiating Resonance Scan...

No temporal echoes detected. All clear!
```

## Development

### Running Tests

```bash
cargo test
```

### Building

```bash
cargo build
```
