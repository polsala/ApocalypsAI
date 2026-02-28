# nightly-uptime-emoji-reporter

Utility that reports system uptime with a whimsical emoji indicating how long the system has been alive.

## Usage

```sh
./src/uptime_report.sh
```

Outputs something like:

```
Uptime: 3d 4h 12m 🌿
```

## How it works

- Reads uptime seconds from `/proc/uptime` (or from the environment variable `UPTIME_MOCK` for testing).
- Converts the seconds into days, hours, and minutes.
- Chooses an emoji based on the number of days:
  - `< 1` day: 🌱
  - `1‑7` days: 🌿
  - `8‑30` days: 🌳
  - `> 30` days: 🌲

## Tests

Run the test suite with:

```sh
bash tests/test_uptime_report.sh
```

The tests mock different uptime values and verify the correct formatted output and emoji.
