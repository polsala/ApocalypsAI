# Nightly Cosmic Dust Collector

## Description

In the vast digital cosmos, files accumulate like cosmic dust, cluttering your precious storage and obscuring vital data. The Nightly Cosmic Dust Collector is your automated janitor, designed to sweep through specified directories, identify ancient digital debris, and offer to jettison it into the void. Keep your systems lean, mean, and ready for whatever the apocalypse throws your way!

## Usage

Run the `collector.py` script with the desired directory and age threshold.

```bash
python src/collector.py --path /path/to/scan --age-days 30 [--dry-run] [--delete]
```

### Arguments:

*   `--path <directory>`: The directory to scan for old files. Required.
*   `--age-days <int>`: Files older than this many days will be flagged as "cosmic dust." Required.
*   `--dry-run`: (Optional) Perform a scan and report files that *would* be deleted, but don't actually delete anything. This is the default behavior if `--delete` is not specified.
*   `--delete`: (Optional) Actually delete the identified "cosmic dust" files. Use with caution!

## Examples

### Dry Run (default)

Scan `/tmp/my_old_logs` for files older than 60 days, without deleting:

```bash
python src/collector.py --path /tmp/my_old_logs --age-days 60
```

### Delete Files

Scan `/var/cache/app` for files older than 7 days and delete them:

```bash
python src/collector.py --path /var/cache/app --age-days 7 --delete
```
