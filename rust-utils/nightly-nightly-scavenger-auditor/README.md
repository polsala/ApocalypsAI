# Nightly Scavenger's Manifest Auditor

A high-performance command-line utility written in Rust to help post-apocalyptic scavengers audit their findings against a desired manifest. This tool quickly identifies missing items from your manifest and any surplus items you've scavenged that weren't on your list.

## Features

*   Compares a manifest file (list of desired items) against a scavenged file (list of found items).
*   Reports items that are in the manifest but not found (or not found in sufficient quantity).
*   Reports items that were scavenged but not present in the manifest (or found in surplus quantity).
*   Handles duplicate items in both manifest and scavenged lists, providing accurate counts.
*   Fast and efficient, ideal for large lists of items.

## Usage

### Prerequisites

To build and run this utility, you need to have Rust and Cargo installed. If you don't have them, you can install them from [rustup.rs](https://rustup.rs/).

### Building

Navigate to the `nightly-scavenger-auditor` directory and build the project:

```bash
cargo build --release
```

The executable will be located at `target/release/nightly-scavenger-auditor`.

### Running

The utility expects two arguments: the path to your manifest file and the path to your scavenged items file. Both files should contain one item per line.

```bash
./target/release/nightly-scavenger-auditor <path_to_manifest_file> <path_to_scavenged_file>
```

**Example:**

Let's say you have `manifest.txt`:
```
Water Bottle
Ration Pack
First Aid Kit
Water Bottle
```

And `scavenged.txt`:
```
Water Bottle
Ration Pack
Scrap Metal
```

Running the auditor:

```bash
./target/release/nightly-scavenger-auditor manifest.txt scavenged.txt
```

Expected Output:

```
--- Scavenger's Manifest Audit Report ---

Missing Items (in manifest, not enough scavenged):
  - Water Bottle (1 missing)
  - First Aid Kit (1 missing)

Surplus Items (scavenged, not in manifest or too many):
  - Scrap Metal (1 surplus)
```

### File Format

*   Each item should be on a new line.
*   Empty lines and lines containing only whitespace will be ignored.
*   Item names are case-sensitive.

## Development and Testing

### Running Tests

To run the automated tests, navigate to the `nightly-scavenger-auditor` directory and execute:

```bash
cargo test
```

The tests are self-contained and use temporary files to simulate different manifest and scavenged item scenarios, ensuring deterministic and offline execution.
