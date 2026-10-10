# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and, when it reaches a dangerous level, issues an apocalyptic warning with random themed messages.

## Usage

```sh
./disk-guardian.sh [threshold]
```

- `threshold` (optional): percentage (0-100) at which to trigger the warning. Default is **80**.

## Example

```sh
$ ./disk-guardian.sh 75
⚠️  Disk usage at 78% – The end is nigh! Beware the looming data deluge.
```

## How it works

The script parses `df -h /` output, extracts the usage percentage, and compares it to the threshold. If the usage exceeds the threshold, it selects a random apocalyptic quote from an internal list and prints it.

## Testing

Run the test suite with:

```sh
./test_disk_guardian.sh
```

The tests mock `df` output to ensure deterministic behavior.
