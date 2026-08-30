# Nightly Scavenged Deduplicator

In the resource-scarce digital wasteland, every byte of storage is precious. The `nightly-scavenged-deduplicator` is your trusty companion for reclaiming valuable space by identifying and purging redundant data echoes across your filesystem.

This utility scans specified directories, calculates cryptographic hashes of files, and reports on duplicates. With caution, it can also automatically delete these duplicates, leaving only one 'original' copy.

## Usage

```bash
./src/deduplicate.sh [OPTIONS] <DIR1> [DIR2...]
```

### Arguments

*   `<DIR1> [DIR2...]`: One or more directories to scan for duplicate files. The script will recursively search within these directories.

### Options

*   `--dry-run`: (Default) Performs a scan and reports all identified duplicates without deleting any files. This is highly recommended for a preview.
*   `--delete`: **USE WITH EXTREME CAUTION!** This option will actually delete all identified duplicate files, keeping only the first encountered instance of each unique file content. There is no undo.
*   `--hash-algo <md5|sha256>`: Specifies the hashing algorithm to use for file comparison. Choose `md5` for faster but less secure hashing, or `sha256` (default) for stronger collision resistance.
*   `--min-size <BYTES>`: Only consider files larger than this specified size. This can speed up scans by ignoring very small files (e.g., `1K`, `1M`, `1G`, `100c` for 100 bytes).
*   `-h`, `--help`: Display the usage instructions and exit.

## Examples

### 1. Dry run to find duplicates in your cache and downloads folders:

```bash
./src/deduplicate.sh --dry-run /var/cache /home/user/downloads
```

### 2. Delete duplicates in an archive directory, using MD5 for speed, only for files larger than 1 Megabyte:

```bash
./src/deduplicate.sh --delete --hash-algo md5 --min-size 1M /mnt/archive/old_data
```

### 3. Scan multiple directories with default SHA256 hashing:

```bash
./src/deduplicate.sh /home/user/documents /home/user/backups /tmp/scavenged_loot
```

## How it Works

1.  **File Discovery**: Uses `find` to locate all regular files within the specified directories.
2.  **Hashing**: For each file, it calculates a cryptographic hash (`sha256sum` or `md5sum`). Files with identical content will have identical hashes.
3.  **Duplicate Identification**: It then groups files by their hashes to identify sets of duplicates.
4.  **Reporting/Purging**: It reports these groups. If `--delete` is specified, it removes all but the first file encountered in each duplicate group.

## Survival Tips

*   Always run with `--dry-run` first to understand what will be deleted.
*   Back up critical data before using `--delete`.
*   Consider using `--min-size` to focus on larger files where space savings are more significant.

May your storage be optimized and your digital footprint light in the coming dawn!
