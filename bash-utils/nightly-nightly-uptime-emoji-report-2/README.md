# nightly-uptime-emoji-report

**What it does**

A tiny Bash script that reads the system's uptime and prints a friendly, emoji‑based status:

- 🟢 **Green circle** – uptime ≥ 1 day (healthy)
- 🟡 **Yellow circle** – uptime ≥ 6 hours but < 1 day (moderate)
- 🔴 **Red circle** – uptime < 6 hours (needs attention)

The script is completely self‑contained, works on any Linux system with `/proc/uptime`, and can be fed a custom uptime file for testing.

**Installation**

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/uptime_report.sh
```

**Usage**

```bash
# Default – reads the real system uptime
./src/uptime_report.sh

# For testing or on non‑Linux platforms you can point it to a custom file
UPTIME_FILE=tests/mock_uptime_1d.txt ./src/uptime_report.sh
```

**Testing**

Run the bundled Bats‑style tests with Bash:

```bash
bash tests/test_uptime_report.sh
```

All tests should pass, confirming the correct emoji is chosen for various uptime scenarios.
