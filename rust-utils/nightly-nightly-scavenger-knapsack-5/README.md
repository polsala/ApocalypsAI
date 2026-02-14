# Nightly Scavenger Knapsack

A tiny Rust command‑line utility that helps you decide which scavenged items to carry when your pack can only hold a limited weight.  It reads a CSV list of items (`name,weight,value`) and prints the optimal selection that maximizes total value while staying within the specified capacity.

## Build

```bash
# Ensure you have Rust and Cargo installed
cargo build --release
```

The binary will be placed at `target/release/nightly-scavenger-knapsack`.

## Usage

```bash
nightly-scavenger-knapsack <capacity> <items.csv>
```

- `<capacity>` – maximum total weight your pack can hold (positive integer).
- `<items.csv>` – path to a CSV file where each line is `name,weight,value`.

### Example

Create a file `items.csv`:

```
Water Bottle,2,3
Canned Food,3,4
First Aid Kit,5,10
Radio,1,2
```

Run the tool:

```bash
nightly-scavenger-knapsack 7 items.csv
```

Output:

```
Selected items (total weight: 7, total value: 15):
- Canned Food
- First Aid Kit
```

## Testing

Run the built‑in test suite with:

```bash
cargo test
```

The tests are deterministic and do not require any external resources.
