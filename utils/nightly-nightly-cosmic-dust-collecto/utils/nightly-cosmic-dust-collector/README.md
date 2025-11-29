# Nightly Cosmic Dust Collector

## Description

The `Nightly Cosmic Dust Collector` is a whimsical-yet-useful utility designed to help maintain the health of your systems by sifting through log files. It acts like a digital prospector, identifying 'cosmic dust' – the errors, warnings, and critical messages that accumulate in your logs – and presenting them in a concise summary.

This tool is particularly useful for quickly assessing the state of applications or services by highlighting recurring issues without requiring a deep dive into individual log files.

## Usage

To use the Cosmic Dust Collector, run the `dust_collector.py` script with the directories you wish to scan. You can also provide custom regex patterns to look for.

```bash
python3 src/dust_collector.py --dirs /var/log/app1 /var/log/app2
```

### Arguments:

*   `--dirs <path> [<path> ...]`: One or more directories to scan for `.log` files. (Required)
*   `--patterns <name>=<regex> [<name>=<regex> ...]`: Optional custom patterns to search for. Each pattern should be in the format `NAME=REGEX`. If not provided, default patterns for `ERROR`, `WARNING`, and `CRITICAL` will be used.

### Example Output:

```
--- Cosmic Dust Collection Report ---

Scanning directories: ['/var/log/app1', '/var/log/app2']

File: /var/log/app1/service.log
  ERROR: 3 occurrences
  WARNING: 1 occurrence

File: /var/log/app2/worker.log
  CRITICAL: 1 occurrence
  ERROR: 0 occurrences
  WARNING: 2 occurrences

--- Summary ---
Total files scanned: 2
Total issues found: 7

Overall Pattern Counts:
  ERROR: 3
  WARNING: 3
  CRITICAL: 1

Dust collection complete. Keep your systems sparkling!
```
