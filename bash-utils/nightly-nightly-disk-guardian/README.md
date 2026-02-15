# nightly-disk-guardian

A whimsical Bash utility that watches a filesystem's disk usage and alerts you with a friendly ASCII guardian when the usage exceeds a configurable threshold.

## Features
- Checks disk usage of any mount point or directory.
- Configurable usage threshold (default 80%).
- Prints a cheerful "guardian" ASCII art when the threshold is crossed.
- Silent success message when everything is fine.

## Installation
Copy `src/disk_guardian.sh` to a location in your `$PATH` and make it executable:

```sh
chmod +x src/disk_guardian.sh
sudo mv src/disk_guardian.sh /usr/local/bin/disk-guardian
```

## Usage
```sh
disk-guardian [options] <path>
```

### Options
- `-t <percent>` – Set the usage threshold (default: 80). Must be an integer between 1 and 100.
- `-h` – Show help.

### Example
```sh
disk-guardian /home
```
If `/home` is 85% full and the default threshold is 80%, you'll see:

```
⚔️  Disk Guardian warns! ⚔️
   Your /home is at 85% capacity.
   Consider cleaning up some space.
   (╯°□°)╯︵ ┻━┻
```

## Testing
Run the bundled tests with:

```sh
bash tests/test_disk_guardian.sh
```

The tests use a mock `df` command to simulate different usage scenarios.

## License
MIT
