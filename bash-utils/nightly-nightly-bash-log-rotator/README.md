# nightly-bash-log-rotator

Utility to automatically compress and purge old log files.

## Usage

```sh
./src/main.sh [-d DIR] [-a AGE] [-r RETENTION] [-n]
```

- `-d DIR` Directory containing logs (default: current directory)
- `-a AGE` Days old to compress (default: 7)
- `-r RETENTION` Days old to delete after compression (default: 30)
- `-n` Dry‑run (show actions without modifying)

## Description

The script finds files older than *AGE* days, compresses them with `gzip`, then removes compressed files older than *RETENTION* days.

## Example

```sh
./src/main.sh -d /var/log/myapp -a 5 -r 20
```

This will compress log files older than 5 days in `/var/log/myapp` and delete any `*.gz` files older than 20 days.
