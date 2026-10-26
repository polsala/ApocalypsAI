## nightly-syslog-filter-sh

A whimsical yet practical bash script designed to sift through the digital detritus of your system logs. It allows you to define custom patterns and keywords to filter out the noise and highlight the messages that truly matter in the post-apocalyptic digital landscape.

### Usage

```bash
./nightly-syslog-filter-sh <log_file> <pattern_file>
```

*   `<log_file>`: The path to the system log file you want to filter.
*   `<pattern_file>`: The path to a file containing patterns (one per line) to search for.

### Example

Let's say you have a log file named `sys.log` and a pattern file named `important_patterns.txt`.

`sys.log`:
```
Oct 26 10:00:00 server kernel: System started successfully.
Oct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2
Oct 26 10:02:10 server CRON[5678]: (root) CMD (command to run)
Oct 26 10:03:00 server kernel: WARNING: Disk usage is high.
Oct 26 10:04:00 server systemd[1]: Started Session 12 of user. 
Oct 26 10:05:00 server kernel: ERROR: Network interface down.
```

`important_patterns.txt`:
```
ERROR
WARNING
CRON
Accepted password
```

Running the script:

```bash
./nightly-syslog-filter-sh sys.log important_patterns.txt
```

Output:

```
Oct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2
Oct 26 10:02:10 server CRON[5678]: (root) CMD (command to run)
Oct 26 10:03:00 server kernel: WARNING: Disk usage is high.
Oct 26 10:05:00 server kernel: ERROR: Network interface down.
```

### Features

*   **Pattern-based filtering**: Use `grep` with multiple patterns for precise filtering.
*   **Case-insensitive matching**: By default, patterns are matched case-insensitively.
*   **Error highlighting**: Optionally, you can add color to the output for critical messages.
*   **Self-contained**: No external dependencies beyond standard bash utilities.

### Testing

Tests are included in the `tests/` directory. They use mock log files and pattern files to ensure deterministic results without relying on actual system logs.
