# nightly-disk-guardian

A whimsical Bash utility that watches your filesystem's disk usage and alerts you with playful messages when any mount point exceeds a configurable threshold (default 80%). Perfect for keeping servers from getting “hungry”.

## Usage

```bash
./src/disk_guardian.sh            # checks real system disks
./src/disk_guardian.sh 85 mock_df.txt   # use custom threshold and mock df output (for testing)
```

## Options

- `THRESHOLD` (optional): percentage (0-100) to trigger warning. Default 80.
- `DF_FILE` (optional): path to a file containing `df -h` output. If omitted, the script runs `df -h` live.

## Exit codes

- `0` – No mount exceeded the threshold.
- `1` – At least one mount exceeded the threshold.

## License

MIT
