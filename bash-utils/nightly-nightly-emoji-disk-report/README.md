# nightly-emoji-disk-report

A whimsical Bash utility that displays disk usage with emojis representing health levels.

## Usage

```sh
./src/main.sh
```

Optional environment variable `EMOJI_THRESHOLD` can be set to a comma‑separated list of thresholds (e.g., "50,80") to customize emoji mapping.

The script parses `df -h` output and prints each filesystem with an emoji:

- 🌱 0‑49% usage
- 🌿 50‑79% usage
- 🌳 80‑94% usage
- 🔥 95‑100% usage

## How it works

The script reads `df -h`, extracts the usage percentage, selects an emoji based on predefined ranges, and prints a formatted line.

## Testing

Run the tests with:

```sh
bash tests/test_main.sh
```
