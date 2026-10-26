# nightly-disk-usage-alert

## Overview

`nightly-disk-usage-alert` is a tiny Bash utility that examines the system's disk usage (via `df -h`) and prints a friendly, emoji‑filled warning whenever a mounted filesystem exceeds a configurable usage threshold.  It’s perfect for crontab‑based health checks or as a quick sanity‑check before a big deployment.

## Features

- **Configurable threshold** – set `THRESHOLD` (percentage) in the environment; defaults to `80`.
- **Mock‑friendly** – if the environment variable `DF_OUTPUT` is defined, the script uses its value instead of calling `df`. This makes automated testing deterministic and offline.
- **Whimsical alerts** – warnings include a warning sign emoji and a light‑hearted message.

## Installation

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/disk_alert.sh
```

## Usage

```bash
# Use default threshold (80%)
./src/disk_alert.sh

# Custom threshold of 90%
THRESHOLD=90 ./src/disk_alert.sh
```

The script prints one line per filesystem that exceeds the threshold, e.g.:

```
⚠️ /dev/sda1 mounted on / is 85% full! Consider cleaning up.
```

If no filesystem exceeds the threshold, the script produces no output and exits with status `0`.

## Testing

A deterministic test suite lives in `tests/`. It sets `DF_OUTPUT` to a static `df`‑like string and verifies that the expected warning is emitted.

Run the tests with:

```bash
bash tests/test_disk_alert.sh
```

## License

MIT © ApocalypsAI
