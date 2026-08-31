# nightly-disk-usage-alert

Utility to monitor disk usage and alert when any filesystem exceeds a configurable threshold.

## Usage

```sh
./disk-usage-alert.sh [threshold]
```

If `threshold` is omitted, it defaults to **80** percent.

The script prints a warning for each filesystem that is over the threshold and exits with status **1**. If all filesystems are below the threshold it exits with status **0**.

## Example

```sh
$ ./disk-usage-alert.sh 75
Warning: /home is 82% full (threshold 75%)
```
