# nightly-uptime-emoji-report

A whimsical Bash utility that reads the system uptime and prints an emoji representing how long the machine has been alive. Short uptimes get a rocket 🚀, daily gets a sun 🌞, weekly gets a cloud with sun 🌤, and long uptimes get a turtle 🐢.

## Usage

```bash
./src/uptime_report.sh          # real uptime
./src/uptime_report.sh 7200     # mock 2 hours uptime (for testing)
```

## How it works

The script reads `/proc/uptime` (first field) unless a numeric argument is supplied. It then selects an emoji based on thresholds.

## License

MIT
