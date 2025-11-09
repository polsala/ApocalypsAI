# Resource Tracker

A whimsical yet practical command‑line utility for keeping an eye on your post‑apocalypse supplies.

## Features

- **Add** a resource with a quantity.
- **Consume** a quantity from an existing resource.
- **List** all tracked resources.
- Persists data in a local JSON file (no network required).

## Installation

The utility is self‑contained and requires only Python 3.11 (standard library).

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Navigate to the utility folder
cd utils/resource-tracker

# Run the CLI (no installation step needed)
python -m src.tracker --help
```

## Usage

```bash
# Add 10 units of food
python -m src.tracker add --name food --amount 10

# Consume 3 units of food
python -m src.tracker consume --name food --amount 3

# List all resources
python -m src.tracker list
```

The data is stored in `resources.json` inside the utility folder by default. You can specify a custom path with `--storage <path>`.

## Testing

```bash
# From the utility root folder
pytest tests
```

All tests run offline and are deterministic.
