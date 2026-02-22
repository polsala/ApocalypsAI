# Nightly Scavenger's Pack Optimizer (nightly-scavenger-pack-opt)

## Summary
This Rust CLI tool helps post-apocalyptic scavengers optimize their haul. Given a list of potential items (each with a name, weight, and survival value) and a maximum carry weight, it calculates the subset of items that maximizes the total survival value without exceeding the weight limit. It's a practical application of the 0/1 Knapsack problem, ensuring you bring back the most valuable goods from the wasteland.

## Features
- **Weight-constrained Optimization**: Maximizes total survival value within a specified carry weight.
- **CSV Input**: Easily define items and their properties using a simple CSV file.
- **Fast & Efficient**: Built with Rust for performance, suitable for large item lists.

## Usage

### Build
To build the utility, navigate to its directory and run:

```bash
cargo build --release
```

The executable will be located at `target/release/nightly-scavenger-pack-opt`.

### Run

```bash
./target/release/nightly-scavenger-pack-opt --max-weight <MAX_WEIGHT> --items-file <PATH_TO_ITEMS_CSV>
```

**Arguments:**
- `--max-weight <WEIGHT>`: The maximum total weight (an integer) the scavenger can carry.
- `--items-file <PATH>`: Path to a CSV file containing the items. The CSV must have `name`, `weight`, and `value` columns.

### Example

Let's say you have an `items.csv` file like this:

```csv
name,weight,value
Rusty Can Opener,1,2
Mutant Rat Jerky,2,5
Pre-War Comic Book,1,3
Intact Water Filter,5,10
Broken Radio,3,1
Medical Kit,4,8
```

And you want to find the optimal haul for a maximum carry weight of `7`:

```bash
./target/release/nightly-scavenger-pack-opt --max-weight 7 --items-file items.csv
```

**Expected Output:**

```
Optimizing for max weight: 7
Selected Items:
- Mutant Rat Jerky (Weight: 2, Value: 5)
- Pre-War Comic Book (Weight: 1, Value: 3)
- Medical Kit (Weight: 4, Value: 8)

Total Weight: 7
Total Value: 16
```

## Input CSV Format
The CSV file must contain a header row with the following columns:

- `name`: (String) The name of the item.
- `weight`: (Integer) The weight of the item.
- `value`: (Integer) The survival value or utility of the item.

Example `items.csv`:

```csv
name,weight,value
Scrap Metal,5,2
Working Flashlight,2,6
Canned Beans,1,3
Rare Holotape,3,10
```

## Development

### Running Tests

```bash
cargo test
```

Tests are self-contained and use mock CSV data to ensure determinism and offline execution.
