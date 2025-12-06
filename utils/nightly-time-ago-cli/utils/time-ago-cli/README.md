# time‑ago‑cli

A lightweight, zero‑dependency utility that turns a timestamp into a friendly “time ago” description.

## Features

- Accepts ISO‑8601 strings (`2023-08-15T12:34:56`) **or** Unix epoch seconds (`1692102896`).
- Outputs human‑readable phrases like `just now`, `5 minutes ago`, `2 days ago`, `3 months ago`, `1 year ago`.
- Optional `--emoji` flag adds a cute emoji that matches the time span.
- Pure Python 3.11, no external packages.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the script directly
python utils/time-ago-cli/src/main.py "2023-08-15T12:34:56"
# With emoji flair
python utils/time-ago-cli/src/main.py "2023-08-15T12:34:56" --emoji
```

## CLI Options

| Option | Description |
|--------|-------------|
| `timestamp` (positional) | ISO‑8601 string or integer epoch seconds. |
| `-e`, `--emoji` | Append an emoji that reflects the age (e.g., 🌱 for minutes, 🌳 for years). |
| `-h`, `--help` | Show help message. |

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/time-ago-cli/tests
```

## License

MIT – see the root `LICENSE` file.
