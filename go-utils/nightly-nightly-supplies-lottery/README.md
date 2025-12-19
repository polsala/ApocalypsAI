# Nightly Supplies Lottery

**Nightly Supplies Lottery** is a tiny Go command‑line utility that helps you decide which survival supply to grab next.  It reads a JSON file describing supplies and their relative weights, then picks one at random using a deterministic seed (so you can reproduce results in tests).

## Features

* Weighted random selection – rarer items get a lower chance.
* Deterministic seeding – useful for scripting and unit tests.
* Zero external dependencies beyond the Go standard library.

## Installation

```bash
# Clone the repository (or copy the generated files into your project)
git clone https://github.com/your‑org/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-supplies-lottery

go build -o supplies-lottery ./src/main.go
```

## Usage

```bash
# Prepare a JSON file describing your supplies
cat > supplies.json <<EOF
[
  {"name": "Water", "weight": 5},
  {"name": "Canned Food", "weight": 3},
  {"name": "First Aid Kit", "weight": 1},
  {"name": "Battery Pack", "weight": 1}
]
EOF

# Run the lottery (optional: provide a seed for reproducibility)
./supplies-lottery -file supplies.json -seed 42
```

The program will output a single line with the chosen supply, e.g.:

```
Water
```

## Flags

* `-file` – Path to the JSON file containing the supplies (required).
* `-seed` – Integer seed for the random number generator. If omitted, the current Unix timestamp is used.

## Testing

Run the unit tests with:

```bash
go test ./...
```

The test suite demonstrates deterministic selection using a fixed seed.
