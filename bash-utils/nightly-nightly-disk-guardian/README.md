# nightly-disk-guardian

**Utility:** Checks the disk usage of a given path and prints a whimsical warning if the usage exceeds a configurable threshold.

## Features
- Simple Bash script with no external dependencies.
- Configurable usage threshold (default 80%).
- Randomly selects a fun warning message when the threshold is crossed.
- Easy to test: the `df` command can be overridden for deterministic unit tests.

## Usage
```bash
./disk_guardian.sh <path> [threshold]
```
- `<path>`: The directory or mount point to inspect (defaults to `/`).
- `[threshold]`: Optional usage percentage (integer) that triggers a warning (default `80`).

### Examples
```bash
# Check root filesystem with default 80% threshold
./disk_guardian.sh /

# Check /var with a custom 70% threshold
./disk_guardian.sh /var 70
```

## How it works
1. The script runs `df -P <path>` to get POSIX‑compatible output.
2. It extracts the usage percentage from the second line.
3. If the usage is below the threshold, it prints a green check‑mark message.
4. If the usage meets or exceeds the threshold, it selects a random whimsical warning from a predefined list and prints it.

## Testing
The script respects the environment variable `DF_CMD`. By setting `DF_CMD` to a custom function, tests can provide deterministic `df` output without touching the real filesystem.

Run the test suite with:
```bash
bash tests/test_disk_guardian.sh
```

---
*Created by the ApocalypsAI Nightly Integrator agent.*
