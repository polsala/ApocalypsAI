# nightly-uptime-emoji-reporter

## Overview

`nightly-uptime-emoji-reporter` is a tiny Bash utility that reads the system's uptime and load average, then prints a friendly message showing how long the system has been up and an emoji representing the system's "mood" based on the load.

- **Low load (< 0.5)** → 😊 (happy)
- **Moderate load (0.5‑1.5)** → 😐 (neutral)
- **High load (>= 1.5)** → 😫 (stressed)

The script is completely self‑contained, has no external dependencies, and includes a test suite that works offline by mocking the `/proc/uptime` and `/proc/loadavg` files.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-uptime-emoji-reporter
```

Make the script executable:

```bash
chmod +x src/uptime_emoji_reporter.sh
```

## Usage

```bash
./src/uptime_emoji_reporter.sh
```

Example output:

```
Uptime: 3 days, 4 hours, 12 minutes - Mood: 😊
```

## Testing

The test suite uses plain Bash and does not require any testing framework. Run the tests with:

```bash
bash tests/test_uptime_emoji_reporter.sh
```

All tests should pass, confirming that the script correctly parses uptime and load values and selects the appropriate emoji.

## License

MIT © ApocalypsAI
