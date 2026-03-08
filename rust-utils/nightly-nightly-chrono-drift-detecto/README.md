# Nightly Chrono-Drift Detector

## Summary
In the ever-shifting realities of the post-apocalyptic landscape, maintaining the integrity of crucial data or resource manifests is paramount. The `nightly-chrono-drift-detector` is a high-performance Rust CLI tool designed to swiftly identify any 'temporal anomalies'—new, deleted, or modified files—between a baseline directory and a current state.

It's like having a temporal scanner for your file system, ensuring that no vital scrap of information vanishes into the void or appears unexpectedly without notice.

## Features
*   **High Performance**: Written in Rust for blazing-fast directory traversal and hashing.
*   **Drift Detection**: Identifies:
    *   **Emergent Chrono-Entities**: Files present in the current directory but not in the baseline.
    *   **Vanished Temporal Echoes**: Files present in the baseline but no longer in the current directory.
    *   **Distorted Chrono-Signatures**: Files present in both, but with altered content (detected via SHA256 hash).
*   **Whimsical Output**: Reports findings with thematic, apocalyptic flair.
*   **Recursive Scan**: Traverses subdirectories to ensure comprehensive coverage.

## Installation

To build and install the `nightly-chrono-drift-detector`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-drift-detector
    ```

2.  **Build the utility:**
    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `target/release/nightly-chrono-drift-detector`. You can also install it to your Cargo bin directory:**
    ```bash
    cargo install --path .
    ```
    This will make `nightly-chrono-drift-detector` available in your PATH.

## Usage

Run the utility by providing two directory paths: a `--baseline` and a `--current` directory.

```bash
nightly-chrono-drift-detector --baseline /path/to/your/baseline_dir --current /path/to/your/current_dir
```

### Arguments:
*   `-b`, `--baseline <PATH>`: The directory representing the known, stable state.
*   `-c`, `--current <PATH>`: The directory representing the state to be checked for anomalies.

### Example:

Let's say you have a `vault_backup` directory (baseline) and a `current_vault` directory (current).

```bash
# Create some test directories and files
mkdir -p /tmp/vault_backup /tmp/current_vault
echo "Old plans" > /tmp/vault_backup/plans.txt
echo "Secret recipe" > /tmp/vault_backup/recipe.md
echo "Old log" > /tmp/vault_backup/logs/day1.log

echo "New plans" > /tmp/current_vault/plans.txt # Modified
echo "New map" > /tmp/current_vault/map.txt # New
mkdir -p /tmp/current_vault/logs
echo "Old log" > /tmp/current_vault/logs/day1.log

nightly-chrono-drift-detector --baseline /tmp/vault_backup --current /tmp/current_vault
```

### Expected Output (example):

```
Scanning for Chrono-Drift...
Baseline established from: /tmp/vault_backup
Current reality check against: /tmp/current_vault

--- Temporal Anomaly Report ---

Emergent Chrono-Entities (New Files):
  - map.txt

Vanished Temporal Echoes (Deleted Files):
  - recipe.md

Distorted Chrono-Signatures (Modified Files):
  - plans.txt
```

If no changes are detected:

```
Scanning for Chrono-Drift...
Baseline established from: /tmp/stable_vault
Current reality check against: /tmp/stable_vault_copy

--- Temporal Anomaly Report ---
No significant chrono-drift detected. Reality remains stable... for now.
```

## Development

To run tests:

```bash
cargo test
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
