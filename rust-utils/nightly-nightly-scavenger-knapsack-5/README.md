# nightly‑scavenger‑knapsack

A whimsical yet practical command‑line utility for the post‑apocalypse survivor who needs to decide which loot to carry.

## What it does

Given a weight capacity (the maximum you can carry) and a list of items (each with a name, weight, and value), the tool solves the classic **0/1 knapsack problem** and returns the optimal set of items that maximizes total value without exceeding the capacity.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build with Cargo
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-scavenger-knapsack
cargo build --release
```

The binary will be located at `target/release/scavenger_knapsack`.

## Usage

```bash
scavenger_knapsack <capacity> <item1> <item2> ...
```

- `<capacity>` – maximum total weight you can carry (positive integer).
- Each `<item>` must be formatted as `name,weight,value` (comma‑separated, no spaces).

### Example

```bash
./target/release/scavenger_knapsack 10 apple,2,5 water,3,8 medkit,5,12
```

**Output**
```
Selected items: apple, water, medkit
Total value: 25
```

In this example the optimal choice is to take *all* three items, exactly filling the capacity of 10 and achieving a total value of 25.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.

## License

MIT – see the root `LICENSE` file.
