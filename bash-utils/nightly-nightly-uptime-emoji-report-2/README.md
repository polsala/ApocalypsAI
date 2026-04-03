# nightly-uptime-emoji-report

Utility that displays the system's uptime along with an emoji that reflects the duration:
- 🌱 less than 1 day
- 🌳 1‑7 days
- 🏔️ more than 7 days

## Usage

```sh
./src/uptime_emoji.sh          # reads actual uptime
./src/uptime_emoji.sh 3600    # mock uptime of 3600 seconds (for testing)
```

## Installation

Make the script executable and run it:

```sh
chmod +x src/uptime_emoji.sh
./src/uptime_emoji.sh
```

## Tests

Run the test suite:

```sh
bash tests/test_uptime_emoji.sh
```
