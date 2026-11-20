# nightly-disk-usage-warden

A tiny Bash utility that checks the root filesystem's disk usage and prints a whimsical status message.

## Usage

```sh
./src/disk_warden.sh            # checks the live system
./src/disk_warden.sh path/to/mock_df.txt   # for testing or custom input
```

The script reads `df -h /` output (or a file) and reports:

- ✅ All clear: usage < 70%
- ⚠️ Warning: 70% ≤ usage < 90%
- 🚨 Critical: usage ≥ 90%

## Testing

Run the provided test suite:

```sh
cd tests && ./test_disk_warden.sh
```
