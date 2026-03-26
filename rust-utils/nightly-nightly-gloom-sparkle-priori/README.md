# Nightly Gloom & Sparkle Prioritizer

## Overview

In the chaotic aftermath, every decision counts. The `nightly-gloom-sparkle-prioritizer` is a Rust CLI tool designed to help you make those critical choices by assigning a 'Survival Score' to your tasks or scavenged items. It takes into account two key, whimsical metrics:

*   **Gloom Factor (1-10):** How utterly dreadful or catastrophic would it be if this item/task were neglected? (1 = minor inconvenience, 10 = immediate doom)
*   **Sparkle Potential (1-10):** How much joy, utility, or rare value does this item/task bring? (1 = barely useful, 10 = a beacon of hope)

The tool then calculates a `Survival Score` (Sparkle Potential - Gloom Factor + 10 to ensure positive scores) and presents a prioritized list, helping you navigate the wasteland with slightly more strategic whimsy.

## Installation

To build and run this utility, you need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  Clone the repository (or navigate to this utility's directory).
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-gloom-sparkle-prioritizer`.

## Usage

Run the tool with an input CSV file:

```bash
nightly-gloom-sparkle-prioritizer <input_file.csv>
```

Or, if running directly with Cargo:

```bash
cargo run --release -- <input_file.csv>
```

### Input File Format

The input file must be a CSV (Comma Separated Values) with three columns, in this order:

`item_name,gloom_factor,sparkle_potential`

*   `item_name`: A string describing the item or task.
*   `gloom_factor`: An integer from 1 to 10.
*   `sparkle_potential`: An integer from 1 to 10.

**Example `scavenge_list.csv`:**

```csv
Rusty Spanner,3,5
Can of Dehydrated Noodles,2,7
Broken Geiger Counter,8,1
Map to the Whispering Wastes,5,9
Singing Wind Chimes,1,3
Mutated Radish Seeds,6,4
```

### Output

The tool will print a prioritized list to standard output, sorted by `Survival Score` in descending order.

**Example Output:**

```
Prioritized Scavenged Items:
----------------------------
1. Map to the Whispering Wastes (Survival Score: 14, Gloom: 5, Sparkle: 9)
2. Can of Dehydrated Noodles (Survival Score: 15, Gloom: 2, Sparkle: 7)
3. Rusty Spanner (Survival Score: 12, Gloom: 3, Sparkle: 5)
4. Singing Wind Chimes (Survival Score: 12, Gloom: 1, Sparkle: 3)
5. Mutated Radish Seeds (Survival Score: 8, Gloom: 6, Sparkle: 4)
6. Broken Geiger Counter (Survival Score: 3, Gloom: 8, Sparkle: 1)
```

## Development

### Running Tests

```bash
cargo test
```
