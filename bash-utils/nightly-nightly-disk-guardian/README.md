# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and warns you with apocalyptic messages when it gets too full.

## Features
- Checks disk usage of `/` (or any mount point you specify).
- Configurable usage threshold (default 80%).
- Emits a random end‑of‑the‑world style warning when the threshold is exceeded.
- Zero dependencies, pure Bash.

## Installation
Copy `src/disk_guardian.sh` to a location in your `$PATH` and make it executable:

```sh
chmod +x src/disk_guardian.sh
sudo mv src/disk_guardian.sh /usr/local/bin/disk-guardian
```

## Usage
```sh
disk-guardian            # checks / with default 80% threshold
disk-guardian /home 90  # checks /home with 90% threshold
```

The script exits with status `0` if usage is below the threshold, otherwise `1`.

## How it works
The script parses the output of `df -P <mount>` to obtain the used percentage.
If the percentage exceeds the threshold, it selects a random warning from a built‑in list and prints it to `stderr`.

## Testing
Run the bundled tests with:

```sh
bash tests/test_disk_guardian.sh
```

The tests mock `df` output via the `DF_OUTPUT` environment variable to ensure deterministic behavior.

## License
MIT
