# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and alerts you with ASCII art when it gets too full. Ideal for keeping servers healthy while adding a touch of fun.

## Usage

```sh
chmod +x src/disk_guardian.sh
./src/disk_guardian.sh
```

You can also simulate usage for testing:

```sh
MOCK_DF_OUTPUT="Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   45G   5G  90% /" ./src/disk_guardian.sh
```

## Options

- `THRESHOLD` environment variable to set a custom warning percentage (default `80`).

## Exit codes

- `0`: Disk usage below threshold.
- `1`: Disk usage at or above threshold.
- `2`: Unable to determine disk usage.
