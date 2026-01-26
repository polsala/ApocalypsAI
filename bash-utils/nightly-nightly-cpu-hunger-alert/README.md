# nightly-cpu-hunger-alert

A whimsical Bash utility that monitors CPU usage and alerts you when it gets too hungry.

## Usage

```bash
./nightly-cpu-hunger-alert [threshold]
```

- `threshold` (optional): CPU usage percentage threshold (default 80). If current usage exceeds this value, the script prints a whimsical warning and exits with status 1.

## Example

```bash
$ ./nightly-cpu-hunger-alert
CPU is calm. Current usage: 22% (threshold 80%)
```

```bash
$ ./nightly-cpu-hunger-alert 50
CPU is feeling hungry! Current usage: 95% (threshold 50%)
```

## License

MIT
