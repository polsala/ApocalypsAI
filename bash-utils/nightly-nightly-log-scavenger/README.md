# Nightly Log Scavenger

## Overview

The `nightly-log-scavenger` is a whimsical yet practical utility designed to help you quickly assess the health of your system by "scavenging" through log files for critical and warning-level events. Instead of dry technical reports, it presents its findings as "Valuable Scraps" (errors, critical failures) and "Questionable Finds" (warnings, notices), giving your system administration a touch of post-apocalyptic charm.

It's perfect for a quick daily check to see if the digital wasteland is quiet or if there are anomalies lurking in the shadows.

## Features

*   **Categorized Findings**: Distinguishes between critical errors ("Valuable Scraps") and warnings/notices ("Questionable Finds").
*   **Customizable Log Path**: Easily specify which log file to scan.
*   **Whimsical Reporting**: Provides a summary with a thematic status message.
*   **Exit Codes**: Returns distinct exit codes for easy integration into automation scripts:
    *   `0`: All clear (no significant issues).
    *   `1`: Questionable finds detected (warnings present).
    *   `2`: Valuable scraps detected (critical errors present).
    *   `1` (for errors): Log file not found or not readable.

## Usage

### Prerequisites

*   A Bash-compatible shell.
*   `grep` utility (standard on most Linux/Unix systems).

### Running the Scavenger

1.  **Make the script executable**:
    ```bash
    chmod +x src/nightly-log-scavenger.sh
    ```

2.  **Run with default log file (e.g., `/var/log/syslog` on many systems)**:
    ```bash
    ./src/nightly-log-scavenger.sh
    ```
    *Note: The default log file path might vary depending on your system. You might need `sudo` to read system logs.*

3.  **Specify a custom log file**:
    ```bash
    ./src/nightly-log-scavenger.sh /var/log/auth.log
    ```
    Or for a specific application log:
    ```bash
    ./src/nightly-log-scavenger.sh /var/log/nginx/error.log
    ```

### Example Output

```
--- Nightly Log Scavenger Report ---
Scanning: /var/log/syslog
------------------------------------

### Valuable Scraps (Critical Events) ###
Keywords: error|critical|fail|denied|fatal|panic
  [SCRAP] Oct 26 08:30:01 hostname kernel: [  123.456789] FATAL: Out of memory
  [SCRAP] Oct 26 09:15:02 hostname systemd[1]: Failed to start Apache HTTP Server.
Total Valuable Scraps Found: 2

### Questionable Finds (Warning/Notice Events) ###
Keywords: warning|warn|notice|timeout|unreachable
  [FIND] Oct 26 08:45:00 hostname systemd[1]: apache.service: Main process exited, code=exited, status=1/FAILURE
  [FIND] Oct 26 10:00:05 hostname sshd[1234]: pam_unix(sshd:auth): authentication failure; logname= uid=0 eu
Total Questionable Finds: 2

--- Scavenging Summary ---
Valuable Scraps (Errors/Critical): 2
Questionable Finds (Warnings/Notices): 2
STATUS: ALERT! High-value scraps detected. Immediate attention recommended!
```

## Development & Testing

### Running Tests

To ensure the scavenger is working as expected, you can run its self-contained tests:

```bash
chmod +x tests/test_nightly-log-scavenger.sh
./tests/test_nightly-log-scavenger.sh
```

The tests create temporary log files to simulate various scenarios (empty logs, logs with errors, logs with warnings, etc.) and verify the script's output and exit codes.
