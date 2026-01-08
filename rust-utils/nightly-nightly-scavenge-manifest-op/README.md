# Nightly Scavenge Manifest Optimizer (nightly-scavenge-manifest-opt)

## Overview

In the post-apocalyptic wasteland, every unit of weight counts. The `nightly-scavenge-manifest-opt` is a high-performance Rust CLI tool designed to help scavengers make critical decisions about what to carry. Given a list of scavenged items, each with a weight and a perceived value, and a maximum carrying capacity, this utility will determine the optimal combination of items to maximize total value without exceeding the weight limit.

It employs a dynamic programming approach (0/1 Knapsack problem) to ensure the most efficient selection, making it a reliable companion for any discerning wasteland wanderer.

## Features

*   **Optimal Item Selection**: Uses a robust algorithm to find the best combination of items.
*   **Configurable Weight Limit**: Easily specify your maximum carrying capacity.
*   **CSV Input**: Reads item data from a simple CSV file (`name,weight,value`).
*   **Fast Execution**: Built with Rust for speed and efficiency.

## Installation

To build and run this utility, you'll need Rust and Cargo installed. If you don't have them, follow the instructions on the [official Rust website](https://www.rust-lang.org/tools/install).

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-scavenge-manifest-opt
    ```
2.  **Build the project:**
    ```bash
    cargo build --release
    ```
    The executable will be located at `target/release/nightly-scavenge-manifest-opt`.

## Usage

Create a CSV file (e.g., `manifest.csv`) with your items, each on a new line, in the format `name,weight,value`.

**Example `manifest.csv`:**

```csv
Rusty Spanner,2,10
Mutant Fungus,1,5
Pre-War PDA,3,25
Intact Can of Beans,1,12
Broken Robot Arm,10,50
Rare Holotape,0,100
```

Then, run the utility, specifying your manifest file and the weight limit:

```bash
./target/release/nightly-scavenge-manifest-opt --manifest manifest.csv --limit 15
```

### Command Line Arguments

*   `-m`, `--manifest <FILE>`: Path to the manifest CSV file.
*   `-l`, `--limit <WEIGHT>`: Maximum weight capacity (an integer).

## Example Output

```
--- Scavenger's Manifest Optimization Report ---
Weight Limit: 15 units
Total Value: 187 credits
Total Weight: 14 units

Chosen Items:
  - Rusty Spanner (Weight: 2, Value: 10)
  - Pre-War PDA (Weight: 3, Value: 25)
  - Intact Can of Beans (Weight: 1, Value: 12)
  - Broken Robot Arm (Weight: 10, Value: 50)
  - Rare Holotape (Weight: 0, Value: 100)
```

## Development & Testing

To run the tests:

```bash
cargo test
```
