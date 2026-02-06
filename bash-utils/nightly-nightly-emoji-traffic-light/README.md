# nightly-emoji-traffic-light

A whimsical Bash utility that reads the system load average and displays a traffic‑light emoji (🟢🟡🔴) indicating low, moderate, or high load. Perfect for a quick status check in your terminal.

## Usage

```sh
./traffic_light.sh          # uses real /proc/loadavg and nproc
# or with custom values for testing
LOADAVG_FILE=./tests/tmp/low CPU_COUNT=4 ./traffic_light.sh
```

## How it works

- Reads the 1‑minute load average from `${LOADAVG_FILE:-/proc/loadavg}`.
- Determines CPU count from `${CPU_COUNT:-$(nproc)}`.
- Compares load per CPU:
  - `< 0.5` → green 🟢 (low)
  - `0.5‑1.0` → yellow 🟡 (moderate)
  - `> 1.0` → red 🔴 (high)

## License

MIT
