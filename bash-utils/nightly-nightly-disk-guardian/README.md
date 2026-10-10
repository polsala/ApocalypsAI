# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and alerts you with an ASCII‑art guardian when usage exceeds a configurable threshold.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional): percentage (0‑100) at which to trigger the alert. Default is **80**.

The script prints the current usage and, if over the threshold, displays a guardian ASCII art with a warning.

## Example

```sh
$ ./src/disk_guardian.sh 75
Disk usage: 78%
⚔️  Guardian says: "Your disk is thirsty! Clean up soon!"
   /\_/\
  ( o.o )
   > ^ <
```

If the usage is below the threshold you get a calm message:

```sh
Disk usage: 45%
All is calm.
```

## Testing

Run the test suite with:

```sh
bash tests/test_disk_guardian.sh
```

The tests mock `df` output to verify both calm and alert behaviours without touching the real filesystem.
