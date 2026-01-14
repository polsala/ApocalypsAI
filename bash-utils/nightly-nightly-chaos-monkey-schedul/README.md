# nightly-chaos-monkey-scheduler

A playful yet powerful Bash utility that introduces controlled chaos to your system at random intervals. Inspired by the legendary Chaos Monkey, this utility helps you stress-test your infrastructure resilience in the most unpredictable ways.

## Features

- Randomly triggers system-level chaos events
- Configurable via environment variables
- Logs all chaos activities with timestamps
- Dry-run mode for testing

## Usage

```bash
# Run with default settings
./chaos-monkey.sh

# Dry run to see what would happen
DRY_RUN=1 ./chaos-monkey.sh

# Set custom chaos probability (1-100)
CHAOS_PROBABILITY=30 ./chaos-monkey.sh
```

## Chaos Events

- CPU stress for random duration
- Temporary network interface down
- Random service restart
- Memory filler process
- Disk I/O stress

## Requirements

- Bash 4+
- stress-ng (for CPU/memory stress)
- iproute2 (for network manipulation)
- systemd (for service management)

## Warning

This tool is designed for testing environments only. Running it in production without understanding the consequences may cause service disruptions.
