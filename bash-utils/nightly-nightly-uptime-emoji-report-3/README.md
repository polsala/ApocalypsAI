# nightly-uptime-emoji-report

A whimsical bash utility that reports system uptime along with an emoji representing the current load.

## Usage

```bash
./src/uptime_emoji.sh
```

You can override values for testing:

```bash
UPTIME_SECONDS=3600 LOADAVG_1=0.2 CORES_OVERRIDE=4 ./src/uptime_emoji.sh
```

## How it works

- Reads uptime from `/proc/uptime` (or the `UPTIME_SECONDS` environment variable for testing).
- Reads the 1‑minute load average from `/proc/loadavg` (or the `LOADAVG_1` environment variable for testing).
- Determines the number of CPU cores via `nproc` (or the `CORES_OVERRIDE` environment variable for testing).
- Chooses an emoji based on load:
  - 🌞 low load (less than 0.5 × cores)
  - 🌤 moderate load (between 0.5 × cores and 1 × cores)
  - 🌩 high load (greater than or equal to 1 × cores)

## License

MIT
