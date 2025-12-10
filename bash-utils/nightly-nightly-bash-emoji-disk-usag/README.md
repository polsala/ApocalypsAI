# nightly-bash-emoji-disk-usage

Utility that displays disk usage (like `df -h`) and appends an emoji that reflects how full each filesystem is.

## Usage

```sh
./src/main.sh [PATH]
```

- `PATH` (optional) – the mount point or directory to check. Defaults to `/`.

The script prints each filesystem line followed by an emoji:

- 🟢 0‑20% full
- 🟡 21‑40% full
- 🟠 41‑60% full
- 🔴 61‑80% full
- 💀 81‑100% full

## How it works

The script runs `df -h` (or a custom command via the `DF_CMD` environment variable for testing), parses the usage percentage, selects an emoji, and prints the line with the emoji.

## Testing

Run the provided test script:

```sh
bash tests/test_main.sh
```
