# Nightly Temporal Rift Repair Kit

A whimsical-yet-useful command-line utility to help you navigate the temporal anomalies of the post-apocalyptic world by converting timestamps between different formats. Whether you're deciphering ancient logs or scheduling future rendezvous, Chronos's Compass will keep your time in order.

## Features

*   Convert Unix timestamps (seconds since epoch) to ISO 8601 UTC strings.
*   Convert ISO 8601 UTC strings to Unix timestamps.
*   Display the current UTC time in both ISO 8601 and Unix formats.

## Installation

This utility is self-contained and written in Python 3.11+.
Simply place `rift_repair.py` in your desired location and make it executable.

```bash
# Example: Make it executable
chmod +x utils/nightly-temporal-rift-repair-kit/src/rift_repair.py
```

## Usage

Run the script directly from the `src` directory.

### Convert Unix Timestamp to ISO 8601 UTC

```bash
python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py 1678886400
# Output: Unix 1678886400 -> ISO 8601 UTC: 2023-03-15T00:00:00+00:00
```

### Convert ISO 8601 UTC String to Unix Timestamp

```bash
python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py --from-iso "2023-03-15T00:00:00+00:00"
# Output: ISO 8601 UTC '2023-03-15T00:00:00+00:00' -> Unix: 1678886400

python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py --from-iso "2023-03-15T00:00:00Z"
# Output: ISO 8601 UTC '2023-03-15T00:00:00Z' -> Unix: 1678886400

python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py --from-iso "2023-03-15T00:00:00"
# Output: ISO 8601 UTC '2023-03-15T00:00:00' -> Unix: 1678886400 (assumes UTC if no timezone specified)
```

### Display Current UTC Time

```bash
python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py --now
# Output:
# Current UTC ISO 8601: 2023-10-27T10:30:45+00:00 (example)
# Current Unix Timestamp: 1698393045 (example)
```

### Help

```bash
python3 utils/nightly-temporal-rift-repair-kit/src/rift_repair.py --help
```
