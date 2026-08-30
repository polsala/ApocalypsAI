# nightly-uptime-emoji-reporter

A whimsical Bash utility that reads the system uptime and reports a mood emoji.

## Usage

./src/main.sh

You can also provide a mock uptime for testing:

UPTIME_MOCK=90000 ./src/main.sh

## How it works

- Reads /proc/uptime (first number is seconds since boot).
- Converts to hours.
- Chooses an emoji based on thresholds:
  - < 24h : 🌱 "Fresh"
  - 24‑72h : 🌤 "Running smoothly"
  - > 72h : 🔥 "Time to reboot!"

## Exit codes

- 0 on success
- 1 if /proc/uptime cannot be read and no mock provided
