# Nightly Scavenge Sorter

A high-performance command-line utility written in Rust to help survivors prioritize their scavenged items. This tool calculates a "survival score" for each item based on its base utility, rarity, and condition, then sorts them to help you decide what to keep, trade, or discard.

## Features

*   **Configurable Scoring**: Items are scored based on:
    *   **Base Utility**: A numerical value representing the item's inherent usefulness (e.g., Water: 10, Rusty Spoon: 1).
    *   **Rarity**: Categorical (Common, Uncommon, Rare, Legendary) with corresponding multipliers.
    *   **Condition**: Categorical (Pristine, Worn, Damaged, Broken) with corresponding multipliers.
*   **Flexible Input**: Reads item data from a simple comma-separated text file.
*   **Sort Order**: Sort items in descending (default) or ascending order of survival score.
*   **Fast**: Built with Rust for optimal performance.

## Installation

1.  **Prerequisites**: Ensure you have [Rust and Cargo](https://www.rust-lang.org/tools/install) installed.
2.  **Clone the repository**:
    ```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-scavenge-sorter
    ```
3.  **Build the utility**:
    ```bash
cargo build --release
    ```
    The executable will be located at `target/release/nightly-scavenge-sorter`.
4.  **Add to PATH (optional)**: For easier access, you might want to add the `target/release` directory to your system's PATH, or copy the executable to a directory already in your PATH (e.g., `/usr/local/bin`).

## Usage

The `nightly-scavenge-sorter` takes an input file and an optional sort order.

```bash
nightly-scavenge-sorter -i <input_file_path> [-o <sort_order>]
```

### Arguments

*   `-i, --input <FILE_PATH>`: **Required**. Path to the text file containing your scavenged items.
*   `-o, --order <ORDER>`: Optional. Specifies the sort order.
    *   `desc` (default): Sorts items from highest to lowest survival score.
    *   `asc`: Sorts items from lowest to highest survival score.

### Input File Format

Each line in the input file should represent one item and follow this comma-separated format:

```
<Item Name>,<Base Utility (u32)>,<Rarity (Common|Uncommon|Rare|Legendary)>,<Condition (Pristine|Worn|Damaged|Broken)>
```

**Example `scavenged_items.txt`:**

```
Water Bottle,10,Common,Pristine
Medical Kit,8,Rare,Worn
Rusty Spoon,1,Common,Broken
Ancient AI Core,20,Legendary,Pristine
Canned Beans,7,Uncommon,Worn
Tattered Map,3,Uncommon,Damaged
Working Flashlight,6,Rare,Damaged
```

### Example Run

```bash
./target/release/nightly-scavenge-sorter -i scavenged_items.txt
```

**Expected Output:**

```
--- Scavenged Item Prioritization ---
[120.00] Ancient AI Core (Utility: 20, Rarity: Legendary, Condition: Pristine)
[20.00] Medical Kit (Utility: 8, Rarity: Rare, Condition: Worn)
[12.00] Water Bottle (Utility: 10, Rarity: Common, Condition: Pristine)
[10.50] Canned Beans (Utility: 7, Rarity: Uncommon, Condition: Worn)
[10.50] Working Flashlight (Utility: 6, Rarity: Rare, Condition: Damaged)
[3.15] Tattered Map (Utility: 3, Rarity: Uncommon, Condition: Damaged)
[0.30] Rusty Spoon (Utility: 1, Rarity: Common, Condition: Broken)
```

## Development & Testing

To run the tests:

```bash
cargo test
```
