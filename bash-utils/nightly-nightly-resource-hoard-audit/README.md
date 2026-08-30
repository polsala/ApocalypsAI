# Nightly Resource Hoard Auditor

The ApocalypsAI Nightly Resource Hoard Auditor is a whimsical-yet-useful Bash utility designed to scan your system for significant resource consumption, playfully dubbed "hoards." It provides a quick overview of the top consumers of disk space, memory, and CPU, helping you identify potential bottlenecks or runaway processes in a post-apocalyptic system landscape.

## Features

-   **Disk Hoard Detection**: Identifies the top 5 largest directories or files on your root filesystem.
-   **Memory Hoard Detection**: Lists the top 5 processes consuming the most RAM.
-   **CPU Hoard Detection**: Highlights the top 5 processes utilizing the most CPU cycles.
-   **Whimsical Reporting**: Presents findings in an "ApocalypsAI" themed report format.

## Usage

To run the auditor, simply execute the script:

```bash
./src/hoard_auditor.sh
```

The script will print a report to standard output, detailing the identified resource hoards.

### Example Output

```
==================================================
 ApocalypsAI Resource Hoard Auditor Report
 Scan Initiated: Mon Oct 26 10:00:00 PDT 2023
==================================================

--- [ Sector: Disk Hoards (Top 5 Largest Directories/Files) ] ---

1.2G    /var/log
800M    /opt/data
500M    /home/user/downloads
200M    /usr/local
100M    /tmp

--- [ Sector: Memory Hoards (Top 5 Processes by RAM) ] ---

USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  5.0 123456 65432 ?        Ss   Jan01   0:01 /usr/bin/hoarder-app --mem-hog
user       10001  0.0  3.5 98765  43210 pts/0    Sl   Feb01   0:05 /usr/bin/another-app
daemon     20002  0.0  2.0 54321  21098 ?        S    Mar01   0:02 /usr/sbin/background-service
root           2  0.0  1.5 1234   5678 ?        S    Jan01   0:00 [kthreadd]
user       10002  0.0  1.0 1111   2222 pts/1    R+   Apr01   0:00 bash

--- [ Sector: CPU Hoards (Top 5 Processes by CPU) ] ---

USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user       10003 15.0  0.5 12345  67890 pts/0    R    May01   0:10 /usr/bin/cpu-burner --intensive
root           4  8.0  0.2 9876   5432 ?        R    Jan01   0:08 [ksoftirqd/0]
user       10004  5.0  0.1 5432   1000 pts/1    S    Jun01   0:03 /usr/bin/idle-process
root           5  2.0  0.1 1111   2222 ?        S    Jan01   0:01 [migration/0]
user       10005  1.0  0.1 999    1111 pts/2    S    Jul01   0:00 sleep 60

==================================================
 Audit Complete. May your resources be ever balanced.
==================================================
```

## Requirements

-   Bash (typically pre-installed on Linux/macOS)
-   `du` utility (Disk Usage)
-   `ps` utility (Process Status)
-   `sort` utility
-   `head` utility
-   `grep` utility

These are standard utilities found on most Unix-like systems.

## Tests

To run the tests, navigate to the `tests/` directory and execute `test_hoard_auditor.sh`:

```bash
cd tests/
./test_hoard_auditor.sh
```

The tests use mocked versions of `du` and `ps` to ensure deterministic and offline execution.
