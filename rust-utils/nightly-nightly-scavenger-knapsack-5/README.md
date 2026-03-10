# Nightly Scavenger Knapsack

Utility to compute the optimal set of scavenged items to carry given a weight capacity. Input is a CSV file with `name,weight,value`.

## Build
```bash
cargo build --release
```

## Run
```bash
cargo run --release -- --capacity <MAX_WEIGHT> <ITEMS_CSV>
```

Example:
```bash
cargo run --release -- --capacity 50 items.csv
```

The program prints the total value and the list of selected items.

## CSV format
Each line should contain three comma‑separated fields:
```
name,weight,value
```
- **name**: identifier of the item (string)
- **weight**: integer weight the item occupies
- **value**: integer usefulness/value of the item

## Tests
Run the test suite with:
```bash
cargo test
```
