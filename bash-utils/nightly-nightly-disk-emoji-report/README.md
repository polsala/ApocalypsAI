# nightly-disk-emoji-report

A whimsical Bash utility that visualizes disk usage per mount point using emojis. Each mount point is displayed with a bar of red (used) and green (free) squares representing usage in 10% increments.

## Usage

```sh
./src/report.sh            # reads live `df -h` output
./src/report.sh /path/to/mock_df.txt   # use a mock file (useful for testing)
```

## Example

```
/dev/sda1 🟥🟥🟥🟩🟩🟩🟩🟩🟩🟩 (30%)
/dev/sda2 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟩 (85%)
tmpfs   🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 (5%)
```

## Tests

Run `bash tests/test_report.sh` to execute deterministic tests.
