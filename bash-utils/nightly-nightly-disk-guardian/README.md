# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and warns you with apocalyptic messages when space runs low.

## Usage

```sh
./src/check_disk.sh
```

It exits with status `0` if usage is below the safe threshold (default **80%**). If above, it prints a warning and exits with status `1`.

You can customize the threshold via the `DISK_THRESHOLD` environment variable.

## How it works

The script runs `df -h /`, parses the usage percentage, and if it exceeds the threshold, selects a random apocalypse‑themed warning from a built‑in list.

## Testing

Run the provided test suite:

```sh
bash tests/test_check_disk.sh
```

All tests are deterministic and use a mocked `df` command, so they work offline.
