# nightly-uptime-emoji-report

**What it does**

A tiny Bash utility that reads the system's load average and number of CPU cores, then prints a friendly message showing the current uptime together with an emoji that reflects the system's "mood":

- **😊** – Light load (≤ 0.5 per core)
- **😐** – Moderate load (> 0.5 and ≤ 1.0 per core)
- **😫** – Heavy load (> 1.0 per core)

The script is completely self‑contained, has no external dependencies, and can be used in cron jobs, status dashboards, or just for a quick terminal check.

**Installation**

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/uptime_emoji_report.sh
```

**Usage**

```bash
./src/uptime_emoji_report.sh
```

You can also feed custom values for testing or automation by setting the environment variables `MOCK_LOAD` and `MOCK_CORES`:

```bash
MOCK_LOAD=0.3 MOCK_CORES=4 ./src/uptime_emoji_report.sh
```

**Running the tests**

```bash
cd tests
bash test_uptime_emoji_report.sh
```

All tests should pass with a zero exit code.
