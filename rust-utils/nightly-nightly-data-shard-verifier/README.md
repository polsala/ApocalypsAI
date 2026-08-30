# Nightly Data Shard Verifier

A high-performance CLI tool for the ApocalypsAI community to verify the integrity of fragmented data "shards" and identify their potential file types, even in a post-apocalyptic data landscape.

## Features

*   **SHA256 Checksum Calculation**: Generates a SHA256 hash for any given file or all files within a directory.
*   **Checksum Verification**: Optionally compares the calculated checksum against an expected value to detect data corruption.
*   **Basic File Type Identification**: Attempts to identify common file types (PNG, JPEG, PDF, ZIP, Plain Text) based on magic bytes, providing a best-effort guess for potentially damaged or incomplete files.
*   **Directory Scanning**: Can process individual files or recursively scan all files within a specified directory.

## Usage

### Prerequisites

To build and run this utility, you need to have Rust and Cargo installed. If you don't have them, you can install them via `rustup`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Build

Navigate to the utility's directory and build it using Cargo:

```bash
cargo build --release
```

The executable will be located at `target/release/nightly-data-shard-verifier`.

### Run

You can run the utility directly from the `target/release/` directory or add it to your system's PATH.

**Verify a single file:**

```bash
./target/release/nightly-data-shard-verifier -p /path/to/your/data_shard.bin
```

**Verify a single file with an expected SHA256 checksum:**

```bash
./target/release/nightly-data-shard-verifier -p /path/to/your/important_log.txt -e "09470125792949a461322744383187212629618147d33742416f40398014841d"
```

The tool will report if the checksum matches or mismatches.

**Scan all files in a directory:**

```bash
./target/release/nightly-data-shard-verifier -p /path/to/your/scavenged_data_cache/
```

This will process each file in the directory, calculating its SHA256 and attempting to identify its type.

### Example Output

```
Processing: /path/to/your/data_shard.bin
  SHA256: 09470125792949a461322744383187212629618147d33742416f40398014841d
  Checksum: MATCHES expected!
  Identified Type: Plain Text
```

## Development & Testing

### Run Tests

```bash
cargo test
```

The tests are self-contained and use temporary files to ensure determinism and isolation.
