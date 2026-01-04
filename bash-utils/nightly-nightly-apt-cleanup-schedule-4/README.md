# nightly-apt-cleanup-scheduler

**What it does**

- Scans the apt package cache (default `/var/cache/apt/archives`).
- Removes `.deb` files older than a configurable number of days (default 7).
- Optionally installs a daily cron job to run the cleanup automatically.
- Sprinkles the output with fun apocalypse‑style warnings so you know the end is near… but your disk stays clean.

**Why it’s useful**

On long‑running systems the apt cache can grow unchecked, eating precious disk space. This tiny script keeps the cache tidy without any heavyweight tools.

**Installation**

```bash
# Clone the utility (or copy the files into your repo)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-apt-cleanup-scheduler

# Make the script executable
chmod +x src/cleanup.sh
```

**Usage**

```bash
# Run a one‑off cleanup (uses the default cache location)
./src/cleanup.sh

# Run with a custom cache directory and age limit
APT_CACHE_DIR=/tmp/fake-apt-cache MAX_DAYS=3 ./src/cleanup.sh

# Install a daily cron job (requires root privileges)
sudo ./src/cleanup.sh --install
```

**Testing**

The test suite creates a temporary fake cache, populates it with files of different ages, runs the script, and asserts that only the old files are removed.

```bash
cd tests
bash test_cleanup.sh
```

**License**

MIT – see the LICENSE file in the repository root.
