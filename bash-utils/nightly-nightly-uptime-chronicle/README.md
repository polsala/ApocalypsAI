# nightly-uptime-chronicle

A whimsical Bash utility that turns system uptime into a fun story.

## Usage

```sh
./uptime-chronicle.sh          # uses real system uptime
./uptime-chronicle.sh 123456   # for testing, provide seconds
```

The script prints a short narrative describing how long the machine has been alive, e.g.:

```
Your server has survived 3 days, 4 hours, and 12 minutes, bravely weathering countless coffee spills.
```

## Options

- **No arguments** – the script reads the actual system uptime from `/proc/uptime`.
- **One numeric argument** – treat the argument as the number of seconds of uptime (useful for testing or for feeding custom values).

## Installation

1. Copy `src/uptime-chronicle.sh` to a directory in your `$PATH`.
2. Make it executable:
   ```sh
   chmod +x /usr/local/bin/uptime-chronicle.sh
   ```
3. Run `uptime-chronicle.sh` whenever you need a morale‑boosting uptime report.

## License

MIT
