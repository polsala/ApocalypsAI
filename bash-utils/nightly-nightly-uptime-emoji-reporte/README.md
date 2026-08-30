# nightly-uptime-emoji-reporter

A whimsical Bash utility that reports system uptime with an appropriate emoji, turning boring uptime numbers into a fun status indicator.

## Usage

```sh
./src/main.sh
```

Optionally, you can pass a custom uptime string for testing:

```sh
./src/main.sh "12345.67 0.00"
```

The script reads `/proc/uptime` by default.

## Emoji mapping

- `< 1 hour` → 🚀 (just launched)
- `1–6 hours` → 🌱 (growing)
- `6–24 hours` → 🐢 (steady)
- `1–7 days` → 🌞 (sunny)
- `> 7 days` → 🌙 (night owl)

## License

MIT
