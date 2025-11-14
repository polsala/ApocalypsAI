# Cosmic Dust Collector

## Unearthing Anomalies in Your Log Files

The universe of your applications generates vast amounts of data, often hidden within log files. But what if these logs contain subtle "cosmic dust bunnies" or alarming "gravitational glitches" that signal impending doom?

The **Cosmic Dust Collector** is a whimsical-yet-powerful utility designed to scan your log files for common error, warning, and exception patterns. It categorizes these anomalies, providing a concise summary report to help you quickly identify and address potential issues before they escalate into a full-blown cosmic catastrophe.

### Features

*   Scans specified log files for predefined error/warning patterns.
*   Categorizes anomalies into "Cosmic Dust Bunnies" (warnings), "Gravitational Glitches" (errors), and "Temporal Anomalies" (exceptions/critical).
*   Generates a summary report with counts and example lines for each anomaly type.
*   Lightweight and self-contained, written in Python.

### Usage

```bash
python src/dust_collector.py <path_to_log_file_1> [path_to_log_file_2 ...]
```

**Example:**

```bash
python src/dust_collector.py /var/log/syslog /app/logs/server.log
```

### Example Output

```
🌌 Cosmic Dust Collector Report 🌌

Scanning: /var/log/syslog
--------------------------------------------------
✨ Cosmic Dust Bunnies (warnings): 2
  - [WARN] Disk space low on /dev/sda1 (85%)
  - [WARNING] Deprecated API usage detected in module 'foo'

💥 Gravitational Glitches (errors): 1
  - [ERROR] Failed to connect to database 'mydb' on port 5432

⏳ Temporal Anomalies (exceptions/criticals): 0
  - No exceptions/criticals detected.

Scanning: /app/logs/server.log
--------------------------------------------------
✨ Cosmic Dust Bunnies (warnings): 0
  - No warnings detected.

💥 Gravitational Glitches (errors): 3
  - [ERROR] User 'admin' failed login attempt from 192.168.1.100
  - [ERROR] File not found: /app/data/config.json

⏳ Temporal Anomalies (exceptions/criticals): 1
  - [CRITICAL] Unhandled exception in main loop: IndexError: list index out of range

---
Summary for all files:
Total Cosmic Dust Bunnies: 2
Total Gravitational Glitches: 4
Total Temporal Anomalies: 1
```

### Development

The `dust_collector.py` script is a standalone Python 3.11 application.
Tests are located in `tests/test_dust_collector.py` and can be run using `pytest` or `python -m unittest`.

```bash
python -m unittest tests/test_dust_collector.py
```
