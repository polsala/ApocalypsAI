# Nightly System Health Check

This whimsical bash script performs a quick, yet surprisingly insightful, health check of your system. It pokes around, asks a few questions, and reports back with a dash of personality.

## Features

*   Checks disk space with a "hoard" metaphor.
*   Monitors running processes with a "critter count" analogy.
*   Verifies network connectivity with a "signal strength" report.
*   Reports on system load with a "burden bearer" metric.
*   Provides a fun, easy-to-understand summary.

## Usage

Simply run the script from your terminal:

```bash
./nightly-sys-health-check.sh
```

## Requirements

*   Bash shell
*   Standard Unix/Linux utilities (e.g., `df`, `ps`, `ping`, `uptime`)

## Testing

Automated tests are included to ensure the script functions as expected. Run them using `bash ./tests/test_sys_health_check.sh`.
