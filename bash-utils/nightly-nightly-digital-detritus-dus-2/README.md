# nightly-digital-detritus-duster

## Summary
The `nightly-digital-detritus-duster` is a whimsical yet practical bash utility designed to help you maintain a pristine digital environment. It identifies and offers to sweep away old, forgotten files – what we affectionately call "digital detritus" or "dust bunnies" – from specified directories, ensuring your systems remain efficient and clutter-free.

## Usage

```bash
./src/detritus_duster.sh <directory> <age_in_days> [OPTIONS]
```

### Arguments
- `<directory>`: The path to the directory you want to clean.
- `<age_in_days>`: Files older than this many days will be considered "detritus".

### Options
- `-d`, `--delete`: **CAUTION!** Actually deletes the identified files. Without this flag, the script performs a dry-run, listing files without deleting them.
- `-v`, `--verbose`: Show more detailed output, including each file being considered.
- `-h`, `--help`: Display this help message.

## Examples

### Dry-run: See what digital dust bunnies are lurking in `/tmp` older than 7 days
```bash
./src/detritus_duster.sh /tmp 7
```

### Verbose dry-run: Get a detailed report of ancient scrolls in `/var/log` older than 30 days
```bash
./src/detritus_duster.sh /var/log 30 -v
```

### Actual cleanup: Sweep away all forgotten artifacts in `/home/user/downloads` older than 90 days
```bash
./src/detritus_duster.sh /home/user/downloads 90 --delete
```

## How it Works
The duster uses the `find` command to locate files based on their modification time. In dry-run mode, it simply lists them. When the `--delete` flag is provided, it proceeds to remove them. It's designed to be simple, efficient, and a little bit fun.

## Installation
This is a standalone bash script. Simply ensure `src/detritus_duster.sh` is executable:
```bash
chmod +x src/detritus_duster.sh
```
Then you can run it directly.
