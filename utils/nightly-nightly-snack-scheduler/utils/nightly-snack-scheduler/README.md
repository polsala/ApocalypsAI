# Nightly Snack Scheduler

## 🍪 Stay Strong, Survivor! 🍪

This utility helps you maintain crucial morale and routine by reminding you about your scheduled 'apocalypse snacks'. Whether it's an emergency protein bar or a morale-boosting muffin, never forget your vital sustenance!

## 🚀 How to Use

1.  **Configure Your Snacks**: Create a `config.json` file in the utility's root directory (next to this README) specifying your snack times and names.
2.  **Run the Scheduler**: Execute the `scheduler.py` script. It will check the current time against your scheduled snacks.

### `config.json` Example:

```json
{
  "snacks": [
    {
      "name": "Emergency Protein Bar",
      "time": "09:00"
    },
    {
      "name": "Hydration Ration (Water)",
      "time": "12:30"
    },
    {
      "name": "Morale-Boosting Muffin",
      "time": "15:45"
    },
    {
      "name": "Night Watch Nosh (Dried Fruit)",
      "time": "20:00"
    }
  ]
}
```

### Running the Script:

```bash
python3 src/scheduler.py
```

### Exit Codes:

*   `0`: Snacks were due and reminders were printed.
*   `2`: No snacks were due at the current time.
*   `1`: An error occurred (e.g., config file not found or malformed).

## 🛠️ Development

### Dependencies

*   Python 3.x (standard library only)

### Running Tests

```bash
python3 -m unittest tests/test_scheduler.py
```
