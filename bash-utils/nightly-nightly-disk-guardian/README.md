# nightly-disk-guardian

A playful Bash utility that monitors the root filesystem's disk usage. If usage exceeds a configurable threshold (default 80%), it prints an ASCII-art warning; otherwise it reports that all is calm.

## Usage

```sh
./src/disk_guardian.sh
```

You can also source the script and call `main` directly from another Bash script.

## Configuration

Set the `THRESHOLD` environment variable to change the warning level (percentage). Example:

```sh
THRESHOLD=90 ./src/disk_guardian.sh
```

## Testing

Run the test suite with:

```sh
bash tests/test_disk_guardian.sh
```
