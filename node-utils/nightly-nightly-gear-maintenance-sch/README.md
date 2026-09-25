# nightly‑gear‑maintenance‑scheduler

A whimsical yet practical Node.js command‑line utility for survivors who need to keep their gear in fighting shape.

## What it does

- Accepts a JSON file describing a list of gear items and their current durability (0‑100%).
- Sorts the items from most damaged to least damaged.
- Assigns a simple maintenance action:
  - **< 30 %** → `Repair ASAP`
  - **30 %‑59 %** → `Inspect soon`
  - **≥ 60 %** → `Good`
- Outputs the prioritized schedule as pretty‑printed JSON.

## Installation

```bash
# Clone the repository (or copy the generated folder) and install dependencies (none required)
cd nightly-gear-maintenance-scheduler
npm install   # no external packages, just for lockfile consistency
```

Make the script executable (optional):

```bash
chmod +x src/main.js
```

## Usage

Create a JSON file describing your gear, e.g. `gear.json`:

```json
[
  {"name": "Radiation Suit", "durability": 85},
  {"name": "Water Filter", "durability": 45},
  {"name": "Plasma Rifle", "durability": 20}
]
```

Run the scheduler:

```bash
node src/main.js gear.json
```

The output will be:

```json
[
  {
    "name": "Plasma Rifle",
    "durability": 20,
    "action": "Repair ASAP"
  },
  {
    "name": "Water Filter",
    "durability": 45,
    "action": "Inspect soon"
  },
  {
    "name": "Radiation Suit",
    "durability": 85,
    "action": "Good"
  }
]
```

## Testing

Run the bundled test script with Node:

```bash
node tests/test_main.js
```

You should see `All tests passed` if everything works.

## License

MIT – feel free to adapt for your own wasteland community!
