# nightly-disk-space-guardian

Utility to scan a directory, report the largest files/directories, and optionally archive old large files.

## Usage

```sh
./disk-space-guardian.sh [-d DIR] [-n N] [-a DAYS]
```

- `-d DIR` : directory to scan (default: current directory)
- `-n N`   : number of top entries to display (default: 5)
- `-a DAYS`: if provided, archive files older than DAYS days that are larger than 10MiB into `archive.tar.gz`.

## Examples

```sh
# Show top 10 consumers in /var
./disk-space-guardian.sh -d /var -n 10

# Archive old large files in /home/user
./disk-space-guardian.sh -d /home/user -a 30
```

## How it works

Uses `du` to compute sizes, `find` to locate old files, and `tar` to create an archive.
