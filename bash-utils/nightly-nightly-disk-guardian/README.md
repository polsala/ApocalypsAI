# nightly-disk-guardian

A whimsical Bash utility that checks the root filesystem disk usage and warns you with an apocalyptic message when space runs low. Ideal for quick cron checks or terminal fun.

## Usage

```sh
./src/disk_guardian.sh
```

The script prints a friendly status. If usage exceeds 80%, it displays a skull ASCII art and a warning.

## Exit codes

- `0`: usage below threshold
- `1`: usage above threshold
- `2`: error determining usage

## License

MIT
