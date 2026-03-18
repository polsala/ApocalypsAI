# nightly-disk-guardian

A whimsical Bash utility that monitors the root filesystem's disk usage. If usage exceeds a configurable threshold (default **80%**), it prints an apocalyptic warning with a random phrase. Perfect for sysadmins who like a dash of drama with their alerts.

## Usage
```bash
./disk_guardian.sh [threshold]
```
- `threshold` – Optional integer (0‑100) representing the usage percent at which the warning triggers. If omitted, defaults to **80**.
- The script examines the output of `df -h /`. For testing you can supply a custom `df` output via the environment variable `DISK_DF_FILE` pointing to a file containing `df`‑style text.

## Example
```bash
# Normal run (uses real df output)
./disk_guardian.sh

# Test with a mock df file (useful for CI)
DISK_DF_FILE=tests/mock_high.txt ./disk_guardian.sh 75
```

## Testing
Run the bundled test suite with:
```bash
bash tests/test_disk_guardian.sh
```
All tests are deterministic and offline; they rely on mock `df` files.
