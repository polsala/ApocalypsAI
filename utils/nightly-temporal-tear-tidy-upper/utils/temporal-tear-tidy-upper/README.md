# Temporal Tear Tidy-Upper

## Mend the Rifts in Your Filesystem!

In the chaotic aftermath, digital detritus accumulates like radioactive dust. The "Temporal Tear Tidy-Upper" is your trusty broom for sweeping away the forgotten files, the temporary anomalies, and the logs of bygone eras that clutter your precious storage. It helps you identify and optionally purge files older than a specified age, restoring order to your digital domain.

### Features:
- **Scan Multiple Directories**: Point it at any number of paths.
- **Age-Based Filtering**: Only target files older than your chosen threshold.
- **Dry Run Mode**: See what would be deleted before committing to the purge.
- **Whimsical Output**: Because even cleanup can be an adventure!

### Usage:

```bash
python src/tidy_upper.py --dirs /path/to/logs /path/to/temp --age 30 --dry-run
```

#### Arguments:
- `--dirs <path1> [<path2> ...]`: One or more directories to scan for old files. **Required.**
- `--age <days>`: Files older than this many days will be flagged. Default is 30 days.
- `--dry-run`: If present, the utility will only list files that *would* be deleted, without actually deleting them.
- `--confirm`: If present (and `--dry-run` is absent), the utility will proceed with deletion without further prompt. **Use with caution!**

### Example:

To list all files older than 60 days in `/var/log` and `~/Downloads` without deleting them:
```bash
python src/tidy_upper.py --dirs /var/log ~/Downloads --age 60 --dry-run
```

To actually delete files older than 7 days in `/tmp` and `/var/tmp` (use with extreme caution!):
```bash
python src/tidy_upper.py --dirs /tmp /var/tmp --age 7 --confirm
```
