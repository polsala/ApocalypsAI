# nightly‑scavenger‑route‑planner

**What it does**

A tiny Rust command‑line tool that reads a JSON file describing points of interest (name and X/Y coordinates) and spits out an ordered list representing a quick scavenger‑run route. It uses a simple *nearest‑neighbor* heuristic – not optimal, but fast and fun for post‑apocalypse planning.

**Why Rust?**

Rust gives us a tiny, zero‑runtime‑dependency binary that can be dropped onto any system – perfect for a rugged utility that might run on a salvaged laptop.

**Build & Run**

```bash
# Clone the repo (or copy the utility folder) and cd into it
cd utils/nightly-scavenger-route-planner

# Build the binary (requires Rust toolchain)
cargo build --release

# Run the tool
./target/release/scavenger-route-planner path/to/locations.json
```

**Input format**

The JSON file must be an array of objects with the following fields:

```json
[
  {"name": "Abandoned Store", "x": 12.3, "y": 45.6},
  {"name": "Radio Tower",   "x": 78.9, "y": 10.1},
  ...
]
```

**Output**

The program prints the route as a comma‑separated list of location names, e.g.:

```
Abandoned Store, Radio Tower, Old Library, ...
```

**Testing**

Run the test suite with:

```bash
cargo test
```

---

*Enjoy plotting your next scavenger run!*
