# Dusty Disk Guardian

A whimsical bash utility that watches your root filesystem disk usage and warns you with apocalyptic messages when usage exceeds a configurable threshold.

## Usage

```sh
./disk_guardian.sh [threshold]
```

- `threshold` (optional) – percentage (default 80) at which the guardian sounds the alarm.

## Example

```sh
$ ./disk_guardian.sh 75
⚠️  The sky darkens as your disk reaches 78% full!
```

If usage is below the threshold:

```sh
$ ./disk_guardian.sh
✅ All clear: disk usage is 42%
```

## Installation

Copy `disk_guardian.sh` to a directory in your `$PATH` and make it executable:

```sh
chmod +x disk_guardian.sh
```

## License

MIT
