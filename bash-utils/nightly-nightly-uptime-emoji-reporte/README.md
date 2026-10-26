# nightly-uptime-emoji-reporter

A whimsical Bash utility that reports the system's uptime accompanied by an emoji that reflects the system's "mood" based on how long it has been running.

## Usage

```sh
./src/uptime_emoji_reporter.sh          # reads actual uptime
./src/uptime_emoji_reporter.sh 7200     # use a custom uptime (seconds) – handy for testing
```

The script prints a line like:

```
Uptime: 2h 0m 🌞
```

## Emoji mapping

- **< 1 hour** – 🚀 (fresh and ready)
- **1–6 hours** – 🌞 (bright and sunny)
- **6–12 hours** – 🌤 (partly cloudy)
- **12–24 hours** – 🌙 (night owl)
- **> 24 hours** – 💤 (time for a nap)

## License

MIT
