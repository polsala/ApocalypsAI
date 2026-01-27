# Uptime Epic Story

A whimsical Bash utility that turns your system's uptime into an epic tale. Perfect for post‑apocalypse terminals.

## Usage

```bash
./src/uptime_story.sh
```

### Options (via environment)

- `UPTIME_MOCK` – provide a mock `/proc/uptime` string for testing, e.g. `"90061.00 0"`.
- `STORY_INDEX` – select which story template to use (0‑based).

## How it works

The script reads `/proc/uptime` (or the mock), converts seconds to days, hours, minutes, and inserts them into a pre‑written narrative.

## Testing

Run the bundled tests:

```bash
bash tests/test_uptime_story.sh
```
