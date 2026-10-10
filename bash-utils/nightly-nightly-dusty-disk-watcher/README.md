# nightly-dusty-disk-watcher

**What it does**

`nightly-dusty-disk-watcher` is a tiny Bash script that monitors the disk usage of a given directory. If the usage exceeds a user‑specified threshold (in megabytes), it prints a warning adorned with a random post‑apocalyptic quote to remind you that the world (or at least your filesystem) is running out of space.

**Why it’s useful**

- Prevents surprise “disk full” errors on servers or workstations.
- Adds a bit of fun to routine sysadmin chores with themed messages.
- Fully self‑contained, no external dependencies.

**Installation**

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/bash-utils/nightly-dusty-disk-watcher
# Make the script executable
chmod +x src/disk_watcher.sh
```

**Usage**

```bash
./src/disk_watcher.sh <directory> <threshold_mb>
```

- `<directory>` – Path to the directory you want to monitor.
- `<threshold_mb>` – Size limit in megabytes. If the directory’s size exceeds this value, a warning is emitted.

**Example**

```bash
# Warn if /var/log grows beyond 500 MiB
./src/disk_watcher.sh /var/log 500
```

**Testing**

The utility includes a deterministic test suite that uses a mock environment variable (`MOCK_DU_OUTPUT`) to simulate `du` output, ensuring the tests run offline.

```bash
cd tests
bash test_disk_watcher.sh
```

**License**

MIT – see the repository root for the full license text.
