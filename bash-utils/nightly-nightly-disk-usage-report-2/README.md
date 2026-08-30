# nightly-disk-usage-report

Utility to list the largest files and directories under a given path.

## Usage

```sh
./src/disk_report.sh [-n COUNT] [PATH]
```

- `-n COUNT` : number of entries to display (default **10**)
- `PATH` : directory to scan (default **current directory**)

The script prints size and path, sorted descending.

## Example

```sh
$ ./src/disk_report.sh -n 5 /var/log
5.1M	/var/log/syslog
2.3M	/var/log/kern.log
... 
```

## Testing

Run the test suite with:

```sh
bash tests/test_disk_report.sh
```
