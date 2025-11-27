# Nightly Temporal Rift Time-Sync

## Overview

In the chaotic aftermath, maintaining a consistent sense of time is paramount. The `nightly-temporal-rift-time-sync` utility helps you keep your system's clock aligned with a reliable external time source, even when temporal rifts threaten to unravel reality. It periodically fetches an external timestamp, compares it to your local system time, and reports any significant drift.

This ensures that your logs are chronologically sound, your scheduled tasks execute precisely, and your perception of time remains unfragmented.

## Usage

To run the time synchronization check, simply execute the `time_sync.py` script:

```bash
python3 src/time_sync.py
```

By default, it will attempt to fetch time from `http://worldtimeapi.org/api/ip`. You can specify a different external time API endpoint using the `--url` argument:

```bash
python3 src/time_sync.py --url https://my-custom-timeserver.com/api/time
```

### Exit Codes

*   `0`: System time is closely aligned (drift less than 1 second).
*   `1`: Significant time drift detected (1 second or more), or failure to retrieve external time.

### Example Output

```
[INFO] Starting Temporal Rift Time-Sync check...
[INFO] Local time: 2023-10-27 10:30:00.123456
[INFO] External time: 2023-10-27 10:30:00.000000
[INFO] System time is closely aligned with external source (drift: 0.123456 seconds).
```

```
[INFO] Starting Temporal Rift Time-Sync check...
[INFO] Local time: 2023-10-27 10:30:00.000000
[INFO] External time: 2023-10-27 10:30:05.000000
[WARNING] Significant time drift detected: -5.000000 seconds (local is behind).
```

## Development

### Dependencies

This utility requires the `requests` library. Install it using pip:

```bash
pip install requests
```

### Running Tests

Tests are located in the `tests/` directory. To run them, navigate to the utility's root directory and execute:

```bash
python3 -m unittest discover tests
```

All tests are deterministic and use mocks to simulate external network requests and system time, ensuring reliable and fast execution.
