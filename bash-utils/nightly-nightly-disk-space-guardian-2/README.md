# nightly-disk-space-guardian

Utility to scan a directory and report the largest files, optionally cleaning up old files. Helpful for keeping servers tidy.

## Usage

```sh
./disk_space_guardian.sh [-d DIR] [-n NUM] [-a AGE_DAYS] [-y]
```

- `-d DIR` : directory to scan (default: current directory)
- `-n NUM` : number of top files to list (default: 10)
- `-a AGE_DAYS` : delete files older than this many days
- `-y` : actually perform deletion (without `-y` only prints what would be deleted)

## Examples

List top 5 biggest files in `/var/log`:

```sh
./disk_space_guardian.sh -d /var/log -n 5
```

Delete files older than 30 days in `/tmp` (dry‑run):

```sh
./disk_space_guardian.sh -d /tmp -a 30
```

Delete them for real:

```sh
./disk_space_guardian.sh -d /tmp -a 30 -y
```

## License

MIT
