# nightly-disk-space-guardian

**Purpose**: Quickly assess the disk usage of the root filesystem and emit a clear warning if usage exceeds a configurable threshold. Ideal for inclusion in cron jobs, CI pipelines, or as a manual sanity‑check before deployments.

## Installation

```bash
# Clone the repository (or copy the utility folder) and make the script executable
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-disk-space-guardian/src
chmod +x check_disk.sh
```

## Usage

```bash
./check_disk.sh            # Uses the default threshold of 80%
./check_disk.sh -t 90      # Custom threshold (e.g., 90%)
```

The script prints a single line indicating the current usage and whether it is within the safe range. It exits with status `0` when usage is below the threshold and `1` when it exceeds the threshold, making it easy to integrate into larger automation workflows.

## Example Output

```
✅ Disk usage is at 57%, below threshold 80%.
```

or

```
⚠️ Disk usage is at 92%, exceeds threshold 80%!
```

## Testing

A deterministic test suite lives in `tests/test_check_disk.sh`. Run it with:

```bash
cd tests
bash test_check_disk.sh
```

All tests should pass, confirming correct parsing and threshold logic.
