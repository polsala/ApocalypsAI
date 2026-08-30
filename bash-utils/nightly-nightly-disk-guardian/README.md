# nightly-disk-guardian

A whimsical bash utility that watches your root filesystem usage and shouts a playful warning when it gets too full.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional) – percentage at which to warn (default **80**).

The script prints a friendly ASCII‑art alarm and exits with code **1** when usage exceeds the threshold, otherwise exits **0**.

## Example

```sh
$ ./src/disk_guardian.sh 75
⚠️  Disk usage is at 78% – time to clean up!
   ____
  / ___)   ___  _   _ _ __ ___   ___
 | |      / _ \| | | | '_ ` _ \ / _ \
 | |___  | (_) | |_| | | | | | |  __/
  \____)  \___/ \__,_|_| |_| |_|\___|
```

## Testing

Run the test suite:

```sh
bash tests/test_disk_guardian.sh
```

The tests use a mock `DF_OUTPUT` environment variable to simulate `df` output, ensuring they run offline and deterministically.
