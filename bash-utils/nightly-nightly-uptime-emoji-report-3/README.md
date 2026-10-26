# nightly-uptime-emoji-report

Utility that displays the system's uptime accompanied by a whimsical emoji representing how long the system has been running.

## Usage

```sh
./src/uptime_emoji.sh
```

The script prints something like:

```
Uptime: 3 days, 4 hours, 12 minutes 🌿
```

## How it works

- Reads uptime in seconds from `/proc/uptime`.
- Converts to days, hours, minutes.
- Chooses an emoji:
  - 🌱 for less than 1 day
  - 🌿 for 1‑7 days
  - 🌳 for more than 7 days

## Testing

Run the test suite:

```sh
bash tests/test_uptime_emoji.sh
```

The tests mock different uptime values to verify correct emoji selection.
