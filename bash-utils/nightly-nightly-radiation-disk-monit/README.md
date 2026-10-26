# Nightly Radiation Disk Monitor

## Overview

`nightly-radiation-disk-monitor` is a tiny Bash utility that checks the root filesystem's disk usage and reports a whimsical *radiation level*:

- **Safe**   🟢  (≤ 70 % used)
- **Elevated** 🟡 (≤ 90 % used)
- **Critical** 🔴 (> 90 % used)

The script is perfect for cron jobs, status dashboards, or just a fun reminder that your server might be “going nuclear”.

## Features

- No external dependencies beyond standard Unix utilities (`bash`, `df`, `awk`).
- Adjustable thresholds are easy to modify in the source.
- Test‑friendly: the `df` command can be overridden via the `DF_CMD` environment variable.

## Installation

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/monitor.sh
```

## Usage

```bash
./src/monitor.sh
```

Typical output:

```
Radiation level: Elevated 🟡 (disk usage 82%)
```

### Custom `df` command (for testing)

You can point the script at any command that mimics `df -P /` output:

```bash
DF_CMD="/path/to/mock_df.sh" ./src/monitor.sh
```

## Testing

A simple Bash test suite lives in `tests/test_monitor.sh`. Run it with:

```bash
bash tests/test_monitor.sh
```

All tests should pass, confirming the correct radiation level is reported for various usage percentages.

## License

This utility is released under the MIT License.
