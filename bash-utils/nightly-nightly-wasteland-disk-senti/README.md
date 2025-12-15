# Wasteland Disk Sentinel

A whimsical Bash utility that watches a directory's disk usage and warns when it approaches a dangerous threshold, perfect for keeping your post‑apocalyptic servers tidy.

## Usage

```sh
./src/main.sh <directory> <size_limit_mb>
```

- `<directory>` – Path to monitor.
- `<size_limit_mb>` – Maximum allowed size in megabytes.

The script reports the current usage as a percentage of the limit and prints a cheerful or alarming message.

## Example

```sh
$ ./src/main.sh /var/log 100
✅ All is calm in the wasteland. (23% of 100MB)
```

When usage exceeds 80 %:

```sh
$ ./src/main.sh /var/log 10
⚠️ The wasteland is overflowing! (92% of 10MB)
```
