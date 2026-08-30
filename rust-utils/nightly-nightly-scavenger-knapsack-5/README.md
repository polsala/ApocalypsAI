# nightly‑scavenger‑knapsack

**What it does**

A tiny Rust command‑line utility that helps a post‑apocalyptic scavenger pick the most valuable items to carry without exceeding a weight limit. It solves the classic 0/1 knapsack problem.

**How to use**

```bash
# Build the binary (requires Rust toolchain)
cargo build --release

# Run the program, feeding it JSON via stdin
cat <<EOF | ./target/release/nightly-scavenger-knapsack
{
  "capacity": 10,
  "items": [
    {"name": "canned‑food", "weight": 3, "value": 5},
    {"name": "water‑bottle", "weight": 4, "value": 4},
    {"name": "first‑aid‑kit", "weight": 5, "value": 7},
    {"name": "radio", "weight": 2, "value": 3}
  ]
}
EOF
```

**Output**

The program prints a JSON array with the names of the selected items, e.g.
```json
["canned‑food","first‑aid‑kit"]
```

**Testing**

Run the test suite with:
```bash
cargo test
```

The tests are deterministic and do not require any external resources.
