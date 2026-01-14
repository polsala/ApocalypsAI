# nightly-disk-usage-emoji

**Summary:** Visualize disk usage of subdirectories using 📦 emojis.

## Description

`nightly-disk-usage-emoji` is a tiny Bash utility that scans a given directory (default current) and prints each immediate subdirectory followed by a number of 📦 emojis proportional to its size. Each 📦 represents 200 KB of disk usage.

## Usage

```sh
./src/disk_usage_emoji.sh [path]
```

- `path` (optional): directory to analyze; defaults to the current directory.

## Example

```sh
$ ./src/disk_usage_emoji.sh /var/log
/var/log/apache2 📦📦📦📦📦📦📦📦📦📦
/var/log/mysql 📦📦📦📦📦📦
/var/log/syslog
```

In the example, `apache2` uses ~2 MB (10 📦), `mysql` ~1.2 MB (6 📦), and `syslog` is smaller than 200 KB, so no emoji is shown.

## Testing

Run the provided test script:

```sh
bash tests/test_disk_usage_emoji.sh
```

The test uses mock data to verify correct emoji scaling.
