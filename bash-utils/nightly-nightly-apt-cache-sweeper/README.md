# nightly-apt-cache-sweeper

Utility to identify and optionally purge stale `.deb` packages from the APT cache, helping keep your system lean in the post‑apocalyptic wasteland.

## Features
- Scan the APT cache for packages older than a configurable number of days.
- Dry‑run mode (default) that only lists stale packages.
- Optional `--delete` flag to actually remove the stale files.
- Respect `APT_CACHE_DIR` environment variable for testing or custom cache locations.

## Installation
```bash
# Clone the utility into your preferred utilities directory
git clone https://github.com/polsala/ApocalypsAI.git
# Assuming you are in the repository root:
cd utils/nightly-apt-cache-sweeper
chmod +x src/main.sh
```

## Usage
```bash
# Dry‑run (default) – list packages older than 30 days
./src/main.sh

# Specify a custom age threshold (e.g., 10 days)
./src/main.sh -d 10

# Actually delete the stale packages
./src/main.sh -d 30 --delete
```

## Testing
```bash
cd tests
bash test_main.sh
```

The test suite creates a temporary mock cache, populates it with files of known ages, and verifies both the dry‑run listing and the deletion behavior.
