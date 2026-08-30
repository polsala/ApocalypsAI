# nightly-disk-usage-whisperer

A whimsical bash utility that scans your system's disk usage and whispers warnings when any partition exceeds a configurable threshold.

## Usage

```sh
./src/main.sh [threshold] [input_file]
```

- `threshold` (optional): usage percentage (integer) at which to warn. Default is **80**.
- `input_file` (optional): path to a file containing `df -h` output. Useful for testing.

If no arguments are given, the script runs `df -h` on the host. For testing you can provide a file containing `df -h` output:

```sh
./src/main.sh 75 sample_df.txt
```

The script will print lines like:

```
/dev/sda1  50G  45G  5G  90%  /   ⚠️ High usage!
```

## How it works

The script parses the output of `df -h`, extracts the usage percentage, and compares it to the threshold. Partitions above the threshold get a warning emoji.

## Tests

Run the test suite with:

```sh
bash tests/test_main.sh
```
