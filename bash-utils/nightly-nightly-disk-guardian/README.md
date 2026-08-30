# nightly-disk-guardian

Utility that checks disk usage and prints whimsical warnings when usage exceeds a threshold.

## Usage

```sh
./src/disk-guardian.sh [options] [mount1 mount2 ...]
```

**Options**

- `-t <percent>`: threshold percentage (default `80`).
- `-h`: show help.

If no mounts are provided, the script checks the root (`/`).

## Example

```sh
./src/disk-guardian.sh -t 75 /
```

Possible output:

```
⚠️  Warning! / is at 82% full. Time to summon more storage spirits!
```

## How it works

The script runs `df -h` for each mount point, extracts the usage percentage, and compares it against the supplied threshold. When the usage meets or exceeds the threshold, a random whimsical phrase is displayed.

## License

MIT
