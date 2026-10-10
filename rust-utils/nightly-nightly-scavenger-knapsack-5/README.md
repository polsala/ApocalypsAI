# nightly‑scavenger‑knapsack

**What it does**

In a world of limited resources, you have a backpack that can only carry a certain weight. You also have a list of scavenged items, each with a *weight* and a *value* (how useful it is for survival). This utility computes the optimal subset of items that maximizes total value without exceeding the backpack’s capacity – the classic 0/1 knapsack problem, but with a post‑apocalyptic flavor.

**Features**

- Reads a JSON file describing the capacity and the available items.
- Outputs a JSON array with the names of the selected items.
- Pure Rust, no external binaries required.
- Deterministic, offline unit tests.

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
# Prepare an input file (example: input.json)
cat > input.json <<EOF
{
  "capacity": 10,
  "items": [
    {"name": "canned beans", "weight": 3, "value": 5},
    {"name": "bottled water", "weight": 2, "value": 4},
    {"name": "first‑aid kit", "weight": 5, "value": 7},
    {"name": "flashlight", "weight": 1, "value": 2}
  ]
}
EOF

# Run the optimizer
./target/release/scavenger_knapsack input.json

# Expected output (JSON array of selected item names)
["canned beans","bottled water","flashlight"]
```

**Input format**

```json
{
  "capacity": <integer>,
  "items": [
    {"name": "string", "weight": <integer>, "value": <integer>},
    ...
  ]
}
```

- `capacity` – maximum total weight the backpack can hold.
- `items` – list of available scavenged items.

**Output format**

A JSON array containing the `name` of each selected item, in the order they appear in the optimal solution.

**Testing**

Run the built‑in test suite with:

```bash
cargo test
```

The tests are deterministic and do not require network access.
