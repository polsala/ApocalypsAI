# Nightly Scavenger Knapsack

**What it does**

In a post‑apocalyptic world you have a limited carrying capacity. This tiny Rust CLI helps you decide which supplies to pack to maximise total value (nutrition, medicine, morale, etc.) while staying within the weight limit.

**Features**

- Reads a plain‑text list of items (`name weight value`)\n- Uses a classic 0/1 knapsack dynamic‑programming algorithm\n- Prints the optimal subset, total weight and total value\n- No external dependencies – just pure Rust

**Installation**

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-scavenger-knapsack

# Build the binary
cargo build --release
```

**Usage**

```bash
# Prepare an items file (one item per line: name weight value)
cat > supplies.txt <<EOF
Water 3 10
Food 2 7
Medkit 5 12
Ammo 4 8
Battery 1 3
EOF

# Run the tool with a capacity of 7 units
./target/release/scavenger-knapsack 7 supplies.txt
```

**Example output**

```
Selected items (total weight 5, total value 17):
- Water (w:3, v:10)
- Food (w:2, v:7)
```

**Testing**

```bash
cargo test
```

All tests run offline and are deterministic.
