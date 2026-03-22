# nightly-disk-guardian

A whimsical Bash utility that watches your disk usage and warns you with apocalyptic messages when space runs low.

## Usage

```sh
./src/disk-guardian.sh [options]
```

### Options

- `-t, --threshold PERCENT`   Set warning threshold (default 80)
- `-h, --help`                Show this help

The script checks the root filesystem and prints a warning with a random apocalypse‑themed phrase if usage exceeds the threshold.

## Example

```sh
$ ./src/disk-guardian.sh
⚠️  Disk usage at 85% – The world is ending in 15% free space!
```

## Testing

Run the test suite:

```sh
bash tests/test_disk_guardian.sh
```
