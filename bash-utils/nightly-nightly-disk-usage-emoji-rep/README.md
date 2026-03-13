# nightly‑disk‑usage‑emoji‑report

A tiny Bash utility that prints the output of `df -h` and adds an emoji indicator for each filesystem based on how much free space is left.

## Why?
When you glance at `df` you have to read the numbers. This script turns the *percentage used* into an intuitive visual cue:

- **🟢** – plenty of space (≥ 80 % free)
- **🟡** – moderate space (50‑79 % free)
- **🔴** – low space (< 50 % free)

It’s handy for quick terminal checks, CI jobs, or adding a dash of whimsy to your daily ops routine.

## Installation
```bash
# Clone the repository (or copy the files) into a directory in your $PATH
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/nightly-disk-usage-emoji-report/src/report.sh /usr/local/bin/disk‑emoji‑report
chmod +x /usr/local/bin/disk‑emoji‑report
```

## Usage
```bash
# Show usage for the root filesystem (default)
$ disk‑emoji‑report

# Show usage for a specific mount point
$ disk‑emoji‑report /home
```

The script works on any Unix‑like system with `df`. It also respects the environment variable `DF_MOCK` – useful for testing – which should contain the exact output you would get from `df -h`.

## Testing
Run the bundled test script:
```bash
cd utils/nightly-disk-usage-emoji-report/tests
bash test_report.sh
```
All tests should pass.
