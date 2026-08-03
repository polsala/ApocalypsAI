# nightly-uptime-emoji-report

A whimsical Bash utility that reports system uptime adorned with an emoji reflecting how long the system has been running.

## Usage

```sh
./src/uptime_emoji.sh          # reads actual system uptime
./src/uptime_emoji.sh 1800    # for testing: provide uptime in seconds
```

The script prints a human‑readable uptime string followed by one of:

- 🐣 less than 1 hour
- 🐔 between 1 hour and 1 day
- 🐓 between 1 day and 1 week
- 🦅 more than 1 week

## Installation

Copy the `src/uptime_emoji.sh` script to a directory in your `$PATH` and make it executable.

## License

MIT
