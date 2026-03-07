# Nightly Temporal Log Report (nightly-temporal-log-report)

Generates a whimsical report of potential temporal anomalies by scanning system logs for time synchronization issues. This utility helps you keep an eye on the stability of your system's clock, ensuring it's not drifting off into another dimension.

## 🌌 Features

*   **Journalctl Whispers**: Scans `journalctl` for entries related to `systemd-timesyncd`, `NTP`, and `Chrony` services, looking for common time synchronization errors.
*   **Dmesg Echoes**: Checks `dmesg` output for kernel-level messages concerning clock stability, drift, or NTP events.
*   **Whimsical Reporting**: Presents findings with a touch of apocalyptic charm, indicating whether the "temporal fabric" is stable or if "potential distortions" are detected.
*   **Bash-Native**: A lightweight script, perfect for quick system checks without heavy dependencies.

## 🚀 Usage

To run the report, simply execute the script:

```bash
./src/main.sh
```

The script will output its findings directly to the console.

### Example Output (No Anomalies)

```
🌌 Nightly Temporal Anomaly Report 🌌
-------------------------------------
Scanning for ripples in the spacetime continuum (aka system time issues)...

✨ All clear! The temporal fabric appears stable. No significant anomalies detected.
   (Or perhaps the anomalies are too subtle for our current instruments...)

-------------------------------------
Report generated on: Tue Jul 26 10:30:00 UTC 2024
```

### Example Output (With Anomalies)

```
🌌 Nightly Temporal Anomaly Report 🌌
-------------------------------------
Scanning for ripples in the spacetime continuum (aka system time issues)...

🌠 Journalctl Whispers (systemd-timesyncd, NTP, Chrony):
-------------------------------------------------
Jul 26 00:00:01 host systemd-timesyncd[123]: Timed out waiting for reply from 1.2.3.4:NTP
Jul 26 00:00:02 host systemd-timesyncd[123]: NTP client failed to set time: Connection refused

🕰️ Dmesg Echoes (kernel time events):
------------------------------------
kernel: clocksource: timekeeping watchdog: Marking clocksource 'tsc' as unstable because it ran backwards.

⚠️ Warning: Potential temporal distortions detected! Further investigation recommended.
   These ripples might indicate a slight desynchronization with the cosmic clock.

-------------------------------------
Report generated on: Tue Jul 26 10:30:00 UTC 2024
```

## 🧪 Testing

The utility includes a self-contained test script to ensure its logic works as expected without requiring actual system log access.

To run the tests:

```bash
./tests/test_main.sh
```

The tests use mock functions to simulate `journalctl` and `dmesg` output, covering scenarios with no anomalies, anomalies in `journalctl`, anomalies in `dmesg`, and anomalies in both.

## 🛠️ Requirements

*   Bash (version 4.0 or higher recommended)
*   `journalctl` (part of systemd, common on Linux) - If not present, the script will gracefully skip this check.
*   `dmesg` (common on Linux) - If not present, the script will gracefully skip this check.
*   `grep`
*   `tail`
*   `command` utility (built-in to Bash)
