# Dusty Disk Watcher

A whimsical bash utility that checks root filesystem disk usage and warns you with post-apocalyptic messages when space runs low.

## Usage

```sh
./dusty_disk_watcher.sh [threshold]
```

- `threshold` (optional) – percentage (default 80) at which the warning triggers.

The script prints a friendly message and exits with code 0.

## Example

```sh
$ ./dusty_disk_watcher.sh
⚠️  Warning! Disk usage at 85% – The wasteland is swelling!
```

## Testing

Run the bundled tests with:

```sh
bash tests/test_dusty_disk_watcher.sh
```
