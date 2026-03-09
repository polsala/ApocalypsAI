# Scavenger Optimize

**nightly-scavenger-optimize** – a tiny Rust CLI that helps post‑apocalypse scavengers choose the most valuable items they can carry.

## What it does
It solves a small 0/1 knapsack problem: given a weight capacity and a list of items (each with weight, value, and a name), it returns the subset of items with the highest total value that fits within the capacity.

## Installation
```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-scavenger-optimize
cargo build --release
```
The binary will be at `target/release/scavenger-optimize`.

## Usage
```bash
scavenger-optimize <capacity> <items>
```
- **capacity** – integer weight limit the scavenger can carry.
- **items** – comma‑separated list of `weight:value:name` entries.

### Example
```bash
./target/release/scavenger-optimize 5 "2:5:water,1:3:food,3:9:medicine"
```
Output:
```
Optimal selection (total value 14):
- water (weight 2, value 5)
- medicine (weight 3, value 9)
```

If no combination fits, the tool reports that nothing can be taken.

## Testing
```bash
cargo test
```
All tests run offline and are deterministic.

## License
MIT – see the repository LICENSE file.
