# nightly-disk-space-guardian

**Purpose**: Keep an eye on your root filesystem and shout out a whimsical, apocalypse‑themed warning when disk usage crosses a user‑defined threshold.

## Features
- Configurable usage threshold (default 80%).
- Works on any Unix‑like system with `df`.
- Deterministic output for testing via the `DF_OUTPUT` environment variable.
- Randomly selects one of four fun warning messages when the threshold is breached.

## Installation
```bash
# Clone the repository (or copy the utility folder) and make the script executable
chmod +x utils/bash-utils/nightly-disk-space-guardian/src/disk_guardian.sh
```

## Usage
```bash
# Check with the default 80% threshold
./src/disk_guardian.sh

# Specify a custom threshold (e.g., 70%)
./src/disk_guardian.sh 70
```

### Exit codes
- `0` – Disk usage is below the threshold.
- `1` – Disk usage exceeds the threshold (warning printed).
- `2` – Unable to parse `df` output.

## Testing
```bash
cd utils/bash-utils/nightly-disk-space-guardian/tests
bash test_disk_guardian.sh
```
All tests should pass.

## Example output
```
✅ Disk usage is safe: 45% (threshold 80%).
```
or when the threshold is crossed:
```
🔥 Your disk is on fire! 92% used.
```
