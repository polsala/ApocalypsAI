# nightly-scavenger-packer

A whimsical CLI tool for post‑apocalypse scavengers. Given a list of found items (name, weight, value) and a maximum carry weight, it computes the optimal set of items to maximize total value using the classic 0/1 knapsack algorithm.

## Usage

```sh
# Build
cargo build --release

# Run with a CSV file of items
cargo run --release -- -w 50 items.csv
```

The CSV file should have a header and rows:

```
name,weight,value
Canned Beans,10,30
Water Bottle,5,20
First Aid Kit,15,50
...
```

The program prints the selected items and total value.

## Tests

```sh
cargo test
```
