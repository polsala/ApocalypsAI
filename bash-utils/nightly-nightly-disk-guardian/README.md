# nightly‑disk‑guardian

**What it does**

`nightly‑disk‑guardian` is a tiny Bash script that checks the disk usage of the root (`/`) filesystem.  If usage exceeds a configurable threshold (default **80 %**), it prints a dramatic warning with ASCII art; otherwise it prints a cheerful message.

**Why it exists**

Running out of disk space on a server can be a silent disaster.  This script gives you a quick, human‑readable alert that can be dropped into cron jobs, monitoring hooks, or just run manually when you feel nostalgic.

**Installation**

```bash
# Clone the repo (or copy the script) into your PATH
mkdir -p ~/bin && cp src/disk_guardian.sh ~/bin/nightly-disk-guardian && chmod +x ~/bin/nightly-disk-guardian
```

**Usage**

```bash
# Run with defaults (checks /, warns at 80%)
nightly-disk-guardian

# Specify a custom threshold (e.g., 90%)
nightly-disk-guardian 90

# For testing, feed a mock `df` output (used by the test suite)
nightly-disk-guardian --mock-output "Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 85G 15G 85% /"
```

**Exit codes**

- `0` – Disk usage is below the threshold (all good).
- `1` – Disk usage exceeds the threshold (warning printed).

**Testing**

The repository includes a simple POSIX‑sh test suite under `tests/`.  Run it with:

```bash
cd tests && sh test_disk_guardian.sh
```

**License**

MIT – see the root `LICENSE` file.
