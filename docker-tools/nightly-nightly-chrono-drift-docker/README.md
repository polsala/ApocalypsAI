# Nightly Chrono-Drift Docker

A whimsical yet highly practical utility for the discerning developer in these temporal-shifting times. The "Chrono-Drift Docker" allows you to execute any command or run a service inside a Docker container with a *simulated* system time, completely isolated from your host machine's clock. Perfect for testing time-sensitive logic, scheduled tasks, certificate expiry, or just experiencing a different temporal reality.

## Features

*   **Temporal Isolation**: Your host's clock remains untouched.
*   **Flexible Time Shifting**: Specify absolute dates/times or relative shifts (e.g., "+10d", "-1h").
*   **Easy Integration**: Just a `docker run` command away.
*   **Reproducible Testing**: Ensure your time-dependent features work as expected across various temporal scenarios.

## How to Build

First, ensure you have Docker installed.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/docker-tools/nightly-chrono-drift-docker
docker build -t nightly-chrono-drift-docker .
```

## How to Use

The utility's entrypoint expects two main arguments:
1.  `FAKE_TIME_SPEC`: The desired time specification. This can be:
    *   An absolute timestamp: `YYYY-MM-DD HH:MM:SS` (e.g., `"2025-01-01 12:00:00"`)
    *   A relative shift: `+Nd` (N days in future), `-Nh` (N hours in past), `+Nm` (N minutes in future), etc. (e.g., `"+1y"`, `"-3w"`, `"+5h"`)
    *   A combination: `"YYYY-MM-DD HH:MM:SS [relative_shift]"` (e.g., `"2024-01-01 00:00:00 +1h"`)
2.  `COMMAND`: The command you wish to execute within the time-shifted container. This should be a single string, often quoted.

### Examples

**1. Check the date in the future:**

```bash
docker run --rm nightly-chrono-drift-docker "2030-07-15 09:00:00" "date"
# Expected output (will vary by timezone, but year/month/day will match):
# Mon Jul 15 09:00:00 UTC 2030
```

**2. Shift time forward by 1 year and run a script:**

```bash
# Assuming you have a script 'my_app/check_expiry.py'
# Create a dummy script for demonstration:
mkdir -p my_app
echo 'import datetime; print(f"Current simulated date: {datetime.datetime.now()}")' > my_app/check_expiry.py

docker run --rm -v "$(pwd)/my_app:/app" nightly-chrono-drift-docker "+1y" "python /app/check_expiry.py"
# Expected output (will be approximately one year from now):
# Current simulated date: 2025-05-15 10:30:00.123456 (example)
```

**3. Run a command with a specific past date:**

```bash
docker run --rm nightly-chrono-drift-docker "2000-01-01 00:00:00" "uptime"
# Expected output (uptime will be based on the simulated start time):
# 00:00:00 up 0 min,  0 users,  load average: 0.00, 0.00, 0.00
```

## How it Works

This utility leverages `faketime`, a powerful tool that intercepts system calls related to time (like `time()`, `gettimeofday()`, `clock_gettime()`) and returns a modified time value. The `entrypoint.sh` script sets up the necessary `LD_PRELOAD` environment variable and executes your command using `faketime`.

## Development & Testing

To run the automated tests:

```bash
cd ApocalypsAI/docker-tools/nightly-chrono-drift-docker
./tests/test_chrono_drift.sh
```
