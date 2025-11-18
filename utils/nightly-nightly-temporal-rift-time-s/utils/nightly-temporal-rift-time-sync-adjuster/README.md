# Nightly Temporal Rift Time-Sync Adjuster

## Overview

In a world where temporal rifts might shift your local clock or communication across disparate survivor enclaves is paramount, the `nightly-temporal-rift-time-sync-adjuster` is your essential tool for chronological coordination. This utility allows you to:

1.  **Display current time** across a specified list of time zones.
2.  **Convert a specific date and time** from one time zone to several others.

No more missed rendezvous or misaligned supply drops! Keep everyone on the same temporal page.

## Installation

This utility is self-contained and requires Python 3.9+ (due to `zoneinfo`).

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-temporal-rift-time-sync-adjuster
    ```
2.  (Optional, but recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  No external dependencies are required beyond Python's standard library.

## Usage

### Display Current Time in Multiple Time Zones

To see the current time in UTC, Europe/London, and America/New_York:

```bash
python3 src/time_sync.py current --zones UTC Europe/London America/New_York
```

Example Output:
```
Current Times:
UTC: 2024-07-20 10:30:00+00:00
Europe/London: 2024-07-20 11:30:00+01:00
America/New_York: 2024-07-20 06:30:00-04:00
```

### Convert a Specific Time Between Time Zones

To convert '2024-07-20 10:00' from UTC to Europe/Berlin and Asia/Tokyo:

```bash
python3 src/time_sync.py convert --time "2024-07-20 10:00" --from-zone UTC --to-zones Europe/Berlin Asia/Tokyo
```

Example Output:
```
Original Time (UTC): 2024-07-20 10:00:00+00:00
Converted Times:
Europe/Berlin: 2024-07-20 12:00:00+02:00
Asia/Tokyo: 2024-07-20 19:00:00+09:00
```

### Available Time Zones

Use standard IANA time zone names (e.g., `America/Los_Angeles`, `Europe/Paris`, `Asia/Tokyo`, `UTC`). A comprehensive list can be found [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

## Development & Testing

To run the tests:

```bash
python3 -m pytest tests/
```
