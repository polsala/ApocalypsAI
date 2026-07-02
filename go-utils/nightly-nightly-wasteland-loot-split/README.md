# Wasteland Loot Splitter

**nightly-wasteland-loot-splitter**

A tiny Go command‑line utility that takes a JSON description of loot items and a number of participants, then distributes the items so that each participant ends up with a roughly equal total value.  The algorithm sorts items by value (high to low) and always gives the next item to the participant with the current lowest total value – a simple yet surprisingly fair approach.

## Usage

```bash
# Build the binary (requires Go 1.22+)
go build -o loot-splitter ./src/main.go

# Run it – pipe JSON input via stdin
cat <<EOF | ./loot-splitter
{
  "items": [
    {"name": "Gold Coin", "value": 100},
    {"name": "Rifle", "value": 250},
    {"name": "Medkit", "value": 80},
    {"name": "Water Bottle", "value": 30}
  ],
  "participants": 3
}
EOF
```

The program prints a JSON object describing each participant's allocation:

```json
{
  "allocations": [
    {
      "participant": 0,
      "items": [
        {"name": "Rifle", "value": 250},
        {"name": "Water Bottle", "value": 30}
      ],
      "total_value": 280
    },
    {
      "participant": 1,
      "items": [
        {"name": "Gold Coin", "value": 100}
      ],
      "total_value": 100
    },
    {
      "participant": 2,
      "items": [
        {"name": "Medkit", "value": 80}
      ],
      "total_value": 80
    }
  ]
}
```

## Testing

Run the bundled tests with:

```bash
go test ./tests
```

All tests are deterministic and use only in‑memory data – no external network calls.
