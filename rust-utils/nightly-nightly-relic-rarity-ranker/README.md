# Nightly Relic Rarity Ranker

## Overview

The `nightly-relic-rarity-ranker` is a command-line utility designed for the discerning scavenger in a post-apocalyptic world. It helps you organize and prioritize your scavenged items (relics) by calculating their perceived rarity and utility scores. This tool is built with Rust for blazing-fast performance, ensuring your inventory decisions are made quickly and efficiently.

Input your findings as a JSON file, and the ranker will output a sorted list, helping you decide what to keep, trade, or discard.

## Features

*   **Relic Scoring**: Calculates rarity and utility scores based on item category, condition, and inherent scarcity.
*   **Customizable Sorting**: Sort results by either rarity or utility.
*   **JSON Input/Output**: Easily integrate with other tools or scripts.
*   **High Performance**: Built with Rust for speed and reliability.

## Installation

To install `nightly-relic-rarity-ranker`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-relic-rarity-ranker
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-relic-rarity-ranker`.
    You can add it to your PATH for easier access:
    ```bash
    sudo cp target/release/nightly-relic-rarity-ranker /usr/local/bin/
    ```

## Usage

### Input File Format

The utility expects a JSON array of relic objects. Each relic should have the following fields:

*   `name`: String (e.g., "Rusty Spanner")
*   `category`: String (e.g., "tool", "weapon", "food", "decoration", "data")
*   `condition`: Integer (0-100, where 100 is pristine)
*   `scarcity_factor`: Integer (0-10, where 10 is extremely rare)

Example `relics.json`:

```json
[
  {
    "name": "Pre-Collapse Data Drive",
    "category": "data",
    "condition": 85,
    "scarcity_factor": 9
  },
  {
    "name": "MRE (Expired)",
    "category": "food",
    "condition": 30,
    "scarcity_factor": 2
  },
  {
    "name": "Working Geiger Counter",
    "category": "tool",
    "condition": 95,
    "scarcity_factor": 8
  },
  {
    "name": "Broken Toy Robot",
    "category": "decoration",
    "condition": 10,
    "scarcity_factor": 1
  }
]
```

### Running the Ranker

```bash
nightly-relic-rarity-ranker --input <path_to_relics.json> [--sort-by <rarity|utility>] [--output-format <json|text>]
```

**Arguments:**

*   `-i, --input <FILE>`: **Required**. Path to the JSON file containing your relics.
*   `-s, --sort-by <FIELD>`: Optional. Sort the output by `rarity` or `utility`. Defaults to `rarity`.
*   `-o, --output-format <FORMAT>`: Optional. Output format: `json` or `text`. Defaults to `text`.

### Examples

1.  Rank relics by rarity (default) and output as text:
    ```bash
    nightly-relic-rarer-ranker -i relics.json
    ```

2.  Rank relics by utility and output as JSON:
    ```bash
    nightly-relic-rarer-ranker -i relics.json -s utility -o json
    ```

## Scoring Logic (Internal)

*   **Rarity Score**: `scarcity_factor * (1.0 + condition / 100.0)`
    *   A higher scarcity factor and better condition lead to higher rarity.
*   **Utility Score**: `base_utility_value_by_category * (condition / 100.0)`
    *   `base_utility_value_by_category`:
        *   `weapon`: 10.0
        *   `tool`: 9.0
        *   `food`: 7.0
        *   `data`: 6.0
        *   `decoration`: 1.0
        *   Any other category: 3.0
    *   A higher base utility for its category and better condition lead to higher utility.

## Development

To run tests:

```bash
cargo test
```
