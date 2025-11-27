# Plant Watering Reminder

**Utility name:** `plant-watering-reminder`

## What it does

Given a list of houseplants, each with a watering interval (in days) and the date it was last watered, the tool tells you which plants need watering *today*.

- Whimsical enough to keep your green thumb happy.
- Useful for anyone who forgets to water their plants.

## Usage

```bash
python -m plant_watering_reminder
```

The script ships with a small example configuration baked into the source. To customise, edit the `DEFAULT_PLANTS` list in `src/water_reminder.py` or import the module and call `plants_to_water` directly.

## How it works

1. Each plant is represented by a `Plant` dataclass (`name`, `interval_days`, `last_watered`).
2. The function `plants_to_water(plants, today)` computes the number of days since `last_watered` and returns the names of plants whose interval has elapsed.
3. The CLI prints the result, one plant per line, or a friendly message if everything is fine.

## Testing

Run the bundled tests with:

```bash
pytest utils/plant-watering-reminder/tests
```

All tests are deterministic and use no external resources.
