# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and warns you with apocalyptic messages when usage exceeds a threshold.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional): percentage (0-100) at which to trigger a warning. Default is **80**.

The script prints a friendly status line. If the usage is above the threshold, it prints a random apocalypse‑themed warning.

## Example

```sh
$ ./src/disk_guardian.sh 75
⚠️  Disk usage at 78% – The sky darkens as your storage swells!
```

## Testing

Run the provided test script:

```sh
bash tests/test_disk_guardian.sh
```
