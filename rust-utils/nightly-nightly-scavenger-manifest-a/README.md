# Nightly Scavenger's Manifest Analyzer

## Overview

The `nightly-scavenger-manifest-analyzer` is a robust and speedy command-line utility built with Rust, designed to help survivors (or meticulous hoarders) quickly process and understand their scavenged inventory. It parses simple text manifests, aggregates item counts, and categorizes them into useful groups like Food, Water, Tools, Components, Medical, and Junk.

No more sifting through handwritten notes or cryptic digital logs! Just feed it your manifest, and get a clear, categorized summary.

## Features

*   **Fast Parsing**: Leverages Rust's performance for quick analysis of large manifests.
*   **Flexible Input**: Reads from a specified file or standard input.
*   **Smart Categorization**: Automatically assigns items to predefined categories based on keywords.
*   **Quantity Aggregation**: Correctly sums up quantities for duplicate items, even with `Nx Item` syntax.
*   **Clear Summary**: Provides a well-formatted output of all items, grouped by category.

## Installation

To install this utility, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-scavenger-manifest-analyzer
    ```

2.  **Build the project:**
    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `target/release/nightly-scavenger-manifest-analyzer`. You can move it to a directory in your PATH for easier access (e.g., `/usr/local/bin`).**
    ```bash
    # Example for Linux/macOS
    sudo cp target/release/nightly-scavenger-manifest-analyzer /usr/local/bin/
    ```

## Usage

The analyzer can take input from a file or directly from standard input.

### Input Format

Each line in your manifest should represent an item. You can specify a quantity using the `Nx Item Name` format, or it will default to `1x`.

Examples:
*   `3x Canned Beans`
*   `Rusty Wrench`
*   `10x Scrap Metal`
*   `Water Bottle`
*   `First Aid Kit`
*   `Mysterious Orb`

### Command Line Options

```
nightly-scavenger-manifest-analyzer --help
```

```
A high-performance CLI tool to parse and summarize scavenged item manifests, categorizing resources and highlighting potential crafting needs.

Usage: nightly-scavenger-manifest-analyzer [OPTIONS]

Options:
  -f, --file <FILE>  Path to the manifest file. If not provided, reads from stdin.
  -h, --help         Print help
  -V, --version      Print version
```

### Examples

1.  **Analyze a manifest file:**

    Create a file named `my_manifest.txt`:
    ```
    2x Canned Peaches
    Rusty Pipe
    5x Copper Wire
    Water Purifier Tablet
    Old Bandage
    Broken Radio
    ```

    Then run:
    ```bash
    nightly-scavenger-manifest-analyzer --file my_manifest.txt
    ```

    Expected Output:
    ```
    --- Scavenger's Manifest Analysis ---

    [Components]
      - Copper Wire: 5

    [Food]
      - Canned Peaches: 2

    [Junk]
      - Broken Radio: 1
      - Rusty Pipe: 1

    [Medical]
      - Old Bandage: 1

    [Water]
      - Water Purifier Tablet: 1
    ```

2.  **Analyze input from stdin (piped from another command or typed directly):**

    ```bash
    echo -e "1x Survival Knife\n3x Dried Meat\n2x Empty Bottle" | nightly-scavenger-manifest-analyzer
    ```

    Expected Output:
    ```
    --- Scavenger's Manifest Analysis ---

    [Food]
      - Dried Meat: 3

    [Tools]
      - Survival Knife: 1

    [Water]
      - Empty Bottle: 2
    ```

## Categories

The utility classifies items into the following categories based on keywords:

*   **Food**: `canned`, `ration`, `berry`, `meat`, `veg`, `dried`
*   **Water**: `water`, `bottle`, `purifier`
*   **Tools**: `wrench`, `hammer`, `knife`, `saw`, `tool`, `pipe`
*   **Components**: `scrap`, `wire`, `gear`, `circuit`, `bolt`, `nut`
*   **Medical**: `bandage`, `medkit`, `antiseptic`, `medicine`, `aid`
*   **Junk**: `rock`, `dirt`, `broken`, `old`, `rusty` (items that might be useful for crafting but are generally low-value or damaged)
*   **Unknown**: Any item not matching the above categories.

Feel free to contribute to expand the keyword list for better categorization!
