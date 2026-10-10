# Nightly Chrono-Hash

`nightly-chrono-hash` is a high-performance command-line utility written in Rust that calculates a unique "chrono-hash" for any given file. This hash is not just a standard content hash; it integrates the file's last modification timestamp, creating a "temporal signature" that helps detect not only data corruption but also subtle temporal drifts or unauthorized modifications to critical files.

## Why Chrono-Hash?

In a post-apocalyptic world, data integrity is paramount, but so is the integrity of time itself. A file might appear unchanged, but if its modification timestamp has been tampered with or subtly shifted by temporal anomalies, a simple content hash won't tell you. Chrono-Hash provides an extra layer of vigilance, ensuring that your critical manifests, survival plans, or ancient data archives haven't been subtly altered by the ravages of time or mischievous temporal echoes.

## Features

*   **Content-Aware Hashing**: Uses SHA256 for robust content integrity.
*   **Temporal Signature**: Incorporates the file's last modification timestamp (in nanoseconds since epoch) into the final hash.
*   **High Performance**: Written in Rust for speed and efficiency.
*   **Simple CLI**: Easy to use with a single command.

## Installation

To install `nightly-chrono-hash`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-chrono-hash
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chrono-hash
cargo build --release
# The executable will be in target/release/nightly-chrono-hash
```

## Usage

Run `nightly-chrono-hash` with the path to the file you want to analyze:

```bash
nightly-chrono-hash <FILE_PATH>
```

### Example

Let's say you have a critical `survival_manifest.txt`:

```bash
echo "Water: 5L\nFood: 10 rations" > survival_manifest.txt
nightly-chrono-hash survival_manifest.txt
# Output might look like: 8a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b
```

If you modify the file:

```bash
echo "Water: 6L\nFood: 10 rations" > survival_manifest.txt
nightly-chrono-hash survival_manifest.txt
# Output will be different due to content change: f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2
```

If the content remains the same but the modification time changes (e.g., by copying the file or a system clock adjustment):

```bash
# Assume survival_manifest.txt has content "Hello World" and a specific mtime
nightly-chrono-hash survival_manifest.txt
# Output: 1234...

# Now, touch the file to update its modification time without changing content
touch survival_manifest.txt
nightly-chrono-hash survival_manifest.txt
# Output: 5678... (will be different from 1234...)
```

This utility is invaluable for maintaining the integrity of your digital assets against both overt corruption and subtle temporal interference.
