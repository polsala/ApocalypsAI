# nightly-uptime-emoji-report

A whimsical Bash utility that reports system uptime along with an emoji reflecting the current load.

## What it does
- Reads the system uptime from `/proc/uptime`.
- Reads the 1‑minute load average from `/proc/loadavg`.
- Chooses an emoji based on the load:
  - **Low load** (`< 0.5`) → 😊
  - **Moderate load** (`< 1.5`) → 😐
  - **High load** (`>= 1.5`) → 😫
- Prints a friendly line such as:
  ```
  Uptime: 3 days, 4 hours, 12 minutes – Load: 0.42 😊
  ```

## Installation
```sh
# Clone the repository (or copy the files) and make the script executable
chmod +x src/uptime_report.sh
```

## Usage
```sh
# Default usage (reads from the real system files)
./src/uptime_report.sh

# For testing or custom sources you can point to alternative files
./src/uptime_report.sh --uptime-file /path/to/mock_uptime --loadavg-file /path/to/mock_loadavg
```

## How it works
The script parses the first number in `/proc/uptime` (seconds) and converts it to days, hours, and minutes. It then extracts the first field from `/proc/loadavg` (the 1‑minute load average) and selects an emoji based on simple thresholds.

## Testing
A minimal test suite lives in `tests/test_uptime_report.sh`. Run it with:
```sh
bash tests/test_uptime_report.sh
```
All tests should pass on any Linux system.
