# nightly-mem-guardian

A whimsical Bash utility that checks system memory health and prints a friendly status message. It reads `/proc/meminfo` (or a supplied file) and reports whether your memory is feeling breezy or cramped.

## Usage

```sh
./mem_guardian.sh            # checks the current system memory
./mem_guardian.sh /path/to/meminfo   # checks a custom meminfo file (useful for testing)
```

The script prints total memory, free memory, and a whimsical status.

## How it works

- Parses `MemTotal` and `MemAvailable` (or `MemFree` if `MemAvailable` missing) from the provided file.
- Calculates the percentage of free memory.
- If free ≥ 30% → prints a happy message.
- Otherwise → prints a warning to consider closing apps.

## Tests

Run the test suite with:

```sh
bash tests/test_mem_guardian.sh
```
