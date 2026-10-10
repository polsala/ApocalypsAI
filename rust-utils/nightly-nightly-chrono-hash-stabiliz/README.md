# Nightly Chrono-Hash Stabilizer

## Overview
`nightly-chrono-hash-stabilizer` is a whimsical-yet-useful command-line utility built in Rust. It helps you assess the 'temporal stability' of a file by repeatedly calculating its SHA256 hash a specified number of times. While a stable file system will always yield identical hashes, this tool simulates observing a file across multiple 'temporal observations' to detect any hypothetical 'temporal drift' or subtle corruption.

It reports the most frequently observed hash (the 'Most Stable Chrono-Hash') and a 'Temporal Stability Score' indicating the percentage of observations that matched this stable hash. This can be a fun way to think about file integrity or a serious tool for systems where data integrity might be subtly compromised over time.

## Features
*   **Temporal Observation**: Re-reads and re-hashes a file multiple times.
*   **Stability Scoring**: Calculates a percentage score based on hash consistency.
*   **Drift Detection**: Identifies if hashes vary across observations.
*   **Whimsical Status Messages**: Provides fun interpretations of the stability score.
*   **High Performance**: Built with Rust for speed and efficiency.

## Installation

To install `nightly-chrono-hash-stabilizer`, you need to have [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-hash-stabilizer
    ```

2.  **Build and install using Cargo:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-chrono-hash-stabilizer` executable to your Cargo bin directory (usually `~/.cargo/bin`), which should be in your system's PATH.

## Usage

```bash
nightly-chrono-hash-stabilizer -f <FILE_PATH> [-i <ITERATIONS>]
```

### Arguments
*   `-f`, `--file <FILE_PATH>`: **(Required)** Path to the file whose chrono-hash you want to stabilize.
*   `-i`, `--iterations <ITERATIONS>`: **(Optional)** Number of temporal observations (hashes) to perform. Defaults to `10`.

### Examples

1.  **Stabilize a file with default iterations (10):**
    ```bash
    nightly-chrono-hash-stabilizer -f my_important_data.txt
    ```

2.  **Stabilize a file with 50 temporal observations:**
    ```bash
    nightly-chrono-hash-stabilizer --file /path/to/my/config.json --iterations 50
    ```

3.  **Handle a non-existent file:**
    ```bash
    nightly-chrono-hash-stabilizer -f non_existent.txt
    # Error: File not found at "non_existent.txt"
    ```

4.  **Handle zero iterations:**
    ```bash
    nightly-chrono-hash-stabilizer -f my_file.log -i 0
    # Error: Iterations must be greater than 0.
    ```

## How it Works (Whimsical Explanation)

In the ApocalypsAI universe, reality can be... shifty. A file that appears one way at one moment might subtly shift its contents the next, due to localized temporal distortions or rogue quantum fluctuations. The Chrono-Hash Stabilizer attempts to peer through these temporal ripples by repeatedly observing the file and hashing its contents.

If all observations yield the same hash, the file is deemed 'Perfectly Stable' – a true anchor in the temporal flux. If some observations differ, it indicates 'Temporal Drift'. The tool then identifies the most common hash as the 'Most Stable Chrono-Hash' and quantifies the drift with a 'Temporal Stability Score'. A low score suggests your file might be experiencing significant reality-bending effects and could benefit from immediate temporal stabilization protocols!

## Development

To build the project locally:

```bash
cargo build
```

To run tests:

```bash
cargo test
```
