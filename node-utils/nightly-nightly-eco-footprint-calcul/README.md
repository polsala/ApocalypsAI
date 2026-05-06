# nightly-eco-footprint-calculator

Calculate a rough personal carbon footprint from everyday activities.  This tiny, self‑contained Node.js CLI is perfect for the post‑apocalyptic survivor who still cares about the planet (or just wants a fun number to brag about).

## Installation

```bash
# Clone the repository (or copy the utility folder) and install dependencies (none required)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-eco-footprint-calculator
chmod +x src/index.js
```

## Usage

```bash
node src/index.js [options]
```

### Options

- `--miles <number>`      Miles driven by car (default: `0`)
- `--kwh <number>`        Electricity usage in kilowatt‑hours (default: `0`)
- `--flight-hours <number>` Flight hours taken (default: `0`)
- `-h, --help`            Show help message

### Example

```bash
node src/index.js --miles 1200 --kwh 350 --flight-hours 5
```

Output:
```
Estimated annual CO₂ emissions: 1,041.50 kg
```

The calculation uses average emission factors:
- **Car travel:** 0.411 kg CO₂ per mile
- **Electricity:** 0.475 kg CO₂ per kWh
- **Flights:** 90 kg CO₂ per flight hour

## Testing

Run the bundled tests with Node:

```bash
node tests/test_index.js
```

All tests should pass, confirming deterministic behavior.

## License

MIT © ApocalypsAI community
