# nightly-disk-guardian

A whimsical Bash utility that watches your root filesystem disk usage and alerts you with an ASCII monster when usage exceeds a threshold, or a sunny smile when all is well.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

- `threshold` (optional): percentage (0-100) at which to trigger the monster alert. Default is 80.

The script exits with status 0 when usage is below the threshold, and 1 when above.

## Example

```sh
$ ./src/disk_guardian.sh 75
🧟‍♂️  Disk usage is at 82% – the monster awakens!
```

## Testing

Run the bundled tests with:

```sh
bash tests/test_disk_guardian.sh
```
