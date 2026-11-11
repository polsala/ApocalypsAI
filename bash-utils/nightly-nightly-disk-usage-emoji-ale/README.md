# nightly-disk-usage-emoji-alert

A tiny Bash utility that scans the output of `df -h` and prints a friendly, emoji‑rich report indicating which mounted filesystems are approaching full capacity.

## Features

- Accepts an optional usage threshold (default **80%**).
- Uses a green 🟢 emoji for healthy mounts and a red 🔴 emoji for mounts that exceed the threshold.
- Works with the standard `df -h` format; can also read from **STDIN** for testing.
- Zero external dependencies – pure Bash.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-disk-usage-emoji-alert
chmod +x src/disk_alert.sh
```

Add the script to your `$PATH` or invoke it directly:

```bash
./src/disk_alert.sh            # uses live `df -h`
./src/disk_alert.sh 90         # warn at 90% usage
```

## Usage

```text
Usage: disk_alert.sh [threshold]
  threshold   Optional integer (1‑100) representing the usage percent that
              triggers a red warning. Default is 80.
```

### Example output

```text
🟢 /dev/sda1   45G   20G   23G   47%  /
🔴 /dev/sdb2   100G   85G   10G   90%  /var
🟢 tmpfs       2.0G   0   2.0G   0%   /run/user/1000
```

## Testing

Run the bundled BATS‑style test script:

```bash
chmod +x tests/test_disk_alert.sh
./tests/test_disk_alert.sh
```

The test feeds a mock `df` output and verifies that the script produces the expected emoji‑annotated lines.

---

*Because even disks deserve a little encouragement.*
