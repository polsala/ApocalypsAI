# Temporal Distortion Stabilizer

## Purpose
In the chaotic dance of the multiverse, ensuring all agents operate on a synchronized temporal plane is paramount. The `Temporal Distortion Stabilizer` is a whimsical-yet-useful command-line utility designed to convert a given datetime string from one timezone to another. It helps ApocalypsAI agents and community members 'stabilize temporal distortions' and maintain chronological coherence across their interdimensional operations.

## Features
- Converts datetimes between specified IANA timezones (e.g., `America/New_York`, `Europe/London`).
- Supports various datetime input formats.
- Provides clear, unambiguous output.

## Installation
This utility requires the `pytz` library. It's recommended to install it in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytz
```

## Usage
Run the utility from the command line, providing the datetime, source timezone, and target timezone:

```bash
python src/timezone_converter.py \
  --datetime "2024-10-27 10:00:00" \
  --from_tz "America/New_York" \
  --to_tz "Europe/London"
```

**Example Output:**

```
Input: 2024-10-27 10:00:00 America/New_York
Output: 2024-10-27 15:00:00 BST+0100
```

### Arguments:
- `--datetime <DATETIME_STRING>`: The datetime string to convert (e.g., `"2024-10-27 10:00:00"`).
- `--from_tz <TIMEZONE_STRING>`: The source IANA timezone (e.g., `"America/New_York"`).
- `--to_tz <TIMEZONE_STRING>`: The target IANA timezone (e.g., `"Europe/London"`).

## Development
To run tests:

```bash
python -m unittest tests/test_timezone_converter.py
```
