# nightly-uptime-emoji-report

A whimsical Bash utility that reports system uptime accompanied by an emoji that reflects how long the system has been running.

## Usage

```sh
./src/uptime-emoji.sh          # reads actual system uptime
./src/uptime-emoji.sh 3600     # mock: 1 hour uptime (for testing)
```

## Emoji mapping

- < 1 hour   : 🐣 (just hatched)
- 1‑6 hours  : 🌞 (bright and fresh)
- 6‑24 hours : 🌤 (daytime)
- 1‑3 days  : 🌥 (getting tired)
- > 3 days   : 🌙 (night owl)

The script prints a single line, e.g.:

```
Uptime: 5h 23m 🌞
```

## How it works

The script either reads `/proc/uptime` (Linux) or accepts a single argument representing seconds for easier testing. It converts seconds to a human‑readable format and selects the appropriate emoji.

## License

MIT
