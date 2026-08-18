# Nightly SSH Known Hosts Deduper

Utility to remove duplicate entries from an SSH `known_hosts` file while preserving comments and the original order. Useful for cleaning up after many SSH connections.

## Usage

```sh
./src/deduper.sh path/to/known_hosts          # prints deduped content to stdout
./src/deduper.sh -i path/to/known_hosts       # edits the file in place
```

The script keeps the first occurrence of each unique host entry (based on the first field) and discards subsequent duplicates. Comment lines (starting with `#`) are left untouched.

## How it works

- Reads the file line‑by‑line.
- Tracks the first field of each non‑comment line.
- Emits the line only if the first field has not been seen before.
- Optionally writes the cleaned content back to the original file (`-i` flag).

## Requirements

- Bash (tested on 4.4+)
- No external dependencies.

## License

MIT © ApocalypsAI Community
