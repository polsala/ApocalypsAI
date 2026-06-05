# nightly‑dusty‑disk‑alert

**Purpose**: Quickly inspect the root (`/`) filesystem usage and emit a fun, apocalypse‑styled warning if the used percentage meets or exceeds a configurable threshold.

## Installation
```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-dusty-disk-alert
# Make the script executable
chmod +x src/dusty_disk_alert.sh
```

## Usage
```bash
# Basic usage – defaults to an 80% threshold
./src/dusty_disk_alert.sh

# Specify a custom threshold (e.g., 90%)
./src/dusty_disk_alert.sh 90
```

### Testing with Mock Data
You can feed a mock `df` output via `--mock` to see how the script reacts without touching the real system:
```bash
cat mock_df.txt | ./src/dusty_disk_alert.sh 70 --mock
```

## How It Works
1. Retrieves disk usage via `df -h /` (or reads from stdin when `--mock` is used).
2. Extracts the used‑percentage column.
3. Compares it against the supplied threshold.
4. If the usage is **≥ threshold**, prints a random apocalypse‑themed warning prefixed with a ⚠️ emoji.
5. Otherwise prints a reassuring ✅ message.

## Testing
Run the bundled tests with Bash:
```bash
cd tests
bash test_dusty_disk_alert.sh
```
All tests should pass, confirming deterministic behaviour.
