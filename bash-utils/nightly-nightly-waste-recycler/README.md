# nightly-waste-recycler

Utility to find and optionally delete files older than *N* days in a given directory.

## Usage

```sh
./main.sh [-d] <directory> <days>
```

- `-d` actually delete the files (default is a dry‑run that only lists them)
- `<directory>` path to the directory you want to scan
- `<days>` age threshold in days; files older than this will be listed/removed

## Examples

```sh
# List files older than 30 days in /var/log (dry‑run)
./main.sh /var/log 30

# Actually delete those files
./main.sh -d /var/log 30
```

## How it works

The script uses `find` with `-mtime` to locate files older than the supplied number of days. In dry‑run mode it simply prints the paths; with `-d` it adds `-delete` to remove them.

## Safety

- The script validates that the directory exists and that the days argument is a non‑negative integer.
- By default it never deletes anything; you must explicitly pass `-d`.

## Testing

See the `tests/` directory for a self‑contained test suite that creates a temporary directory, populates it with files of known ages, and verifies both dry‑run and delete behaviours.
