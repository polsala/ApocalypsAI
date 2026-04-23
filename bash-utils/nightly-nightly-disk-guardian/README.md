# nightly-disk-guardian

A whimsical bash utility that watches your root filesystem usage and warns you with apocalyptic messages when space runs low.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional) – percentage (0‑100) at which to trigger the warning. Default is **80**.

The script prints a friendly warning with a random apocalypse‑themed quote if usage exceeds the threshold, otherwise it reports that all is well.

## Example

```sh
$ ./src/disk_guardian.sh
[OK] Disk usage at 45% – the world is still safe.
```

## Testing

Run the test suite:

```sh
bash tests/test_disk_guardian.sh
```
