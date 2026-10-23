# nightly-disk-guardian

A whimsical Bash utility that monitors the root filesystem's disk usage and, when usage exceeds a configurable threshold, prints an apocalypse‑themed warning with ASCII art.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional) – percentage (0‑100) at which to trigger the warning. Default is **80**.

The script exits with code **0** if usage is below the threshold, **1** otherwise.

## Example

```sh
$ ./src/disk_guardian.sh 75
⚠️  Disk usage at 78% – The world is ending!
   ____
  /____\   *BOOM*
```

## Testing

Run the test suite with:

```sh
bash tests/test_disk_guardian.sh
```

The tests mock disk usage values to verify both the safe and warning paths.
