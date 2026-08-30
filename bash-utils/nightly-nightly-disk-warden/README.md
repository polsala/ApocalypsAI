# nightly-disk-warden

A whimsical Bash utility that watches your root filesystem usage and alerts you with a playful message when it approaches a dangerous level.

## Usage

```sh
./src/disk_warden.sh [threshold]
```

- `threshold` (optional) – percentage (0‑100) at which to warn. Default: **80**.

The script prints a green "All clear" message if usage is below the threshold, otherwise a red warning with ASCII art.

## Tests

Run the test suite:

```sh
bash tests/test_disk_warden.sh
```

The tests mock `df` output, so they run safely on any system.
