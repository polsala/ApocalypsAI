# Nightly Chronosync Crystal Calibrator

The ApocalypsAI collective operates across various temporal rifts and geographical locations. To ensure perfect synchronization and prevent temporal paradoxes (or just missed meetings), the Chronosync Crystal Calibrator is here!

This utility helps you convert times between different time zones and suggests optimal meeting slots, making cross-timezone coordination a breeze.

## Features

*   **List Time Zones**: Get a selection of common IANA time zone names.
*   **Convert Time**: Translate a specific date and time from one time zone to another.
*   **Suggest Meetings**: Propose common meeting start times (e.g., 9 AM, 1 PM, 5 PM UTC) and show their equivalents in a list of specified time zones, highlighting if they fall within typical working hours (8 AM - 6 PM local time).

## Installation

This utility is self-contained and written in Python 3.11+. It uses only standard library modules (`datetime`, `zoneinfo`, `argparse`).

1.  Navigate to the `utils/nightly-chronosync-crystal-calibrator/` directory.
2.  The main script is `src/chronosync.py`.

## Usage

All commands are run via `python src/chronosync.py <command> [arguments]`.

### 1. List Common Time Zones

To see a selection of commonly used time zone names (based on IANA Time Zone Database):

```bash
python src/chronosync.py list
```

Example Output:
```
Available Time Zones (selection):
- America/Los_Angeles
- America/New_York
- Asia/Shanghai
- Asia/Tokyo
- Australia/Sydney
- Europe/Berlin
- Europe/London
- UTC

For a full list, refer to IANA Time Zone Database names.
```

### 2. Convert Time Between Zones

To convert a specific datetime from a source time zone to a target time zone:

```bash
python src/chronosync.py convert "<YYYY-MM-DD HH:MM>" <FROM_TZ> <TO_TZ>
```

*   `<YYYY-MM-DD HH:MM>`: The date and time string (e.g., "2024-07-20 14:30").
*   `<FROM_TZ>`: The source time zone (e.g., "America/New_York").
*   `<TO_TZ>`: The target time zone (e.g., "Europe/London").

Example: Convert 10:00 AM New York time to London time on July 20, 2024.
```bash
python src/chronosync.py convert "2024-07-20 10:00" America/New_York Europe/London
```

Example Output:
```
Original: 2024-07-20 10:00 America/New_York
Converted: 2024-07-20 15:00 BST+0100
```

### 3. Suggest Meeting Times

To get suggestions for meeting times across multiple time zones, showing their local equivalents and if they fall within typical working hours (8 AM - 6 PM local):

```bash
python src/chronosync.py suggest <TZ1> <TZ2> [TZ3 ...]
```

*   `<TZ1> <TZ2> [TZ3 ...]`: A space-separated list of time zones to consider.

Example: Suggest meeting times for teams in New York, London, and Tokyo.
```bash
python src/chronosync.py suggest America/New_York Europe/London Asia/Tokyo
```

Example Output:
```
Meeting Time Suggestions (8 AM - 6 PM local considered working hours):

--- If meeting starts at 09:00 UTC ---
  America/New_York: 05:00 EDT-0400 (❌ Outside Working Hours)
  Europe/London: 10:00 BST+0100 (✅ Working Hours)
  Asia/Tokyo: 18:00 JST+0900 (✅ Working Hours)

--- If meeting starts at 13:00 UTC ---
  America/New_York: 09:00 EDT-0400 (✅ Working Hours)
  Europe/London: 14:00 BST+0100 (✅ Working Hours)
  Asia/Tokyo: 22:00 JST+0900 (❌ Outside Working Hours)

--- If meeting starts at 17:00 UTC ---
  America/New_York: 13:00 EDT-0400 (✅ Working Hours)
  Europe/London: 18:00 BST+0100 (✅ Working Hours)
  Asia/Tokyo: 02:00 JST+0900 (❌ Outside Working Hours)
```

## Running Tests

To ensure the Chronosync Crystal Calibrator is functioning correctly, navigate to the utility's root directory and run the tests:

```bash
python -m unittest tests/test_chronosync.py
```
