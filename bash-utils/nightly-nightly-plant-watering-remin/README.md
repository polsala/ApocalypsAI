# nightly-plant-watering-reminder

**A whimsical Bash utility that reminds you when to water your houseplants and tracks watering history.**

## Features

- Stores plant watering schedules in a simple CSV file.
- Calculates which plants need watering based on the current date.
- Lists upcoming watering dates for all plants.
- Marks a plant as watered (updates the CSV in‑place).
- Fully testable with deterministic date overrides.

## Installation

```bash
# Clone the repository (or copy the utility folder) and make the script executable
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/bash-utils/nightly-plant-watering-reminder
chmod +x src/reminder.sh
```

Optionally add the script to your `PATH`:

```bash
ln -s $(pwd)/src/reminder.sh /usr/local/bin/plant-reminder
```

## Usage

The script reads a CSV file (default: `~/.plant_watering.csv`).  Each line has the format:

```
plant_name,last_watered_iso,interval_days
```

Example:

```
Fern,2023-09-01,7
Cactus,2023-09-10,30
```

### Commands

- **List all plants with next watering date**
  ```bash
  ./src/reminder.sh --list
  ```

- **Check a single plant**
  ```bash
  ./src/reminder.sh Fern
  ```

- **Mark a plant as watered today**
  ```bash
  ./src/reminder.sh --water Fern
  ```

- **Help**
  ```bash
  ./src/reminder.sh --help
  ```

### Testing

The utility is designed to be deterministic for tests by allowing the current date to be overridden with the `DATE_OVERRIDE` environment variable (format `YYYY-MM-DD`).  See `tests/test_reminder.sh` for an example.

## License

MIT © ApocalypsAI community
