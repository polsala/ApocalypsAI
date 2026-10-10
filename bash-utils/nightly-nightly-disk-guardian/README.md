# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem usage and alerts you with ASCII art when space runs low. Perfect for sysadmins who like a little fun with their monitoring.

## Usage

```sh
./src/disk_guardian.sh
```

You can also simulate disk usage for testing by setting the `MOCK_DF` environment variable to a custom `df` output line, e.g.:

```sh
MOCK_DF="Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   85G   15G  85% /" ./src/disk_guardian.sh
```

## How it works

The script runs `df -h /` (or uses `MOCK_DF` if set), extracts the usage percentage, and prints a happy sun emoji if usage < 80%, otherwise a dramatic skull ASCII art.

## Tests

Run the test suite:

```sh
bash tests/test_disk_guardian.sh
```
