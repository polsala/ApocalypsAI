# Nightly Relic Registry CLI

`nightly-relic-registry-cli` is a high-performance command-line utility crafted to help you catalog and assess the 'decay status' of files (or 'relics') within a specified directory. It recursively scans, calculates SHA256 checksums, records modification times, and assigns a whimsical decay status based on age.

## Features

*   **Recursive Scanning**: Traverses directories to find all files.
*   **SHA256 Checksums**: Ensures the integrity of your digital relics.
*   **Decay Status**: Assigns a fun status (Pristine, Weathered, Decaying, Dust) based on the file's last modification time.
*   **JSON Output**: Generates a structured JSON file for easy parsing and integration.

## Installation

To install `nightly-relic-registry-cli`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-relic-registry-cli
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-relic-registry-cli
cargo build --release
# The executable will be found at target/release/nightly-relic-registry-cli
```

## Usage

Run the utility by specifying the input directory and an optional output file.

```bash
nightly-relic-registry-cli --input-dir /path/to/your/relics --output-file my_relic_manifest.json
```

### Arguments

*   `-i`, `--input-dir <DIR>`: The directory to scan for relics. (Required)
*   `-o`, `--output-file <FILE>`: The output file for the relic registry in JSON format. Defaults to `relic_registry.json`. (Optional)

### Example

```bash
# Scan your 'documents' folder and save the registry to 'documents_registry.json'
nightly-relic-registry-cli -i ~/documents -o documents_registry.json

# Scan the current directory and save to the default output file
nightly-relic-registry-cli -i .
```

## Output Format

The output is a JSON array of relic entries, each with the following structure:

```json
[
  {
    "id": "RELIC-1",
    "path": "/path/to/your/relics/document.txt",
    "filename": "document.txt",
    "checksum_sha256": "a1b2c3d4e5f6...",
    "last_modified": "2023-10-27T10:00:00Z",
    "decay_status": "Pristine",
    "size_bytes": 12345
  },
  {
    "id": "RELIC-2",
    "path": "/path/to/your/relics/archive/old_photo.jpg",
    "filename": "old_photo.jpg",
    "checksum_sha256": "f6e5d4c3b2a1...",
    "last_modified": "2018-05-15T14:30:00Z",
    "decay_status": "Weathered",
    "size_bytes": 987654
  }
]
```

### Decay Status Definitions

*   `Pristine`: Last modified less than 1 year ago.
*   `Weathered`: Last modified 1 to 5 years ago.
*   `Decaying`: Last modified 5 to 10 years ago.
*   `Dust`: Last modified more than 10 years ago.
*   `Unknown`: Modification time could not be retrieved.

## Development

To contribute or modify the tool:

1.  Clone the repository.
2.  Navigate to `rust-utils/nightly-relic-registry-cli`.
3.  Run tests: `cargo test`
4.  Build: `cargo build`
5.  Run: `cargo run -- -i <input_dir> -o <output_file>`
