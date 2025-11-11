# Chronos's Compass

A whimsical-yet-useful utility for navigating the temporal currents of our distributed world. Chronos's Compass helps you keep track of time across different timezones, ensuring you're always in sync with your global collaborators, or just curious about what time it is on the other side of the digital apocalypse.

## Features

*   **Global Time Display**: Show the current time in a list of specified timezones.
*   **Time Conversion**: Convert a specific date and time from one timezone to another.
*   **Pure Python**: Self-contained and uses only standard library modules (`datetime`, `zoneinfo`).

## Installation

This utility is self-contained. Simply navigate to the `utils/chronos-compass/src/` directory and run the `chronos_compass.py` script.

## Usage

### Display Current Time in Multiple Timezones

To see the current time in UTC, New York, and Tokyo:

```bash
python src/chronos_compass.py --display UTC America/New_York Asia/Tokyo
```

Example output:

```
Current Time Across Zones:
UTC: 2023-10-27 10:30+00:00
America/New_York: 2023-10-27 06:30-04:00
Asia/Tokyo: 2023-10-27 19:30+09:00
```

### Convert a Specific Time Between Timezones

To convert "2023-10-27 14:00" from "Europe/London" to "America/Los_Angeles":

```bash
python src/chronos_compass.py --convert "2023-10-27 14:00" --from-tz Europe/London --to-tz America/Los_Angeles
```

Example output:

```
Conversion:
2023-10-27 14:00 Europe/London  ->  2023-10-27 06:00 America/Los_Angeles
```

### Available Timezones

You can use any valid IANA timezone name (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`, `UTC`). A comprehensive list can be found [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

## Development

### Running Tests

To run the tests, navigate to the `utils/chronos-compass/` directory and execute:

```bash
python -m unittest tests/test_chronos_compass.py
```
