# Nightly Syslog Whisperer

A whimsical yet useful bash utility to monitor your system's syslog for specific keywords. It filters messages and presents them in a slightly more poetic, less alarming way, like whispers from the system's soul.

## Usage

```bash
./nightly-syslog-whisperer.sh <keyword1> [keyword2] ...
```

**Arguments:**

*   `<keyword1>`, `[keyword2]`, ...: One or more keywords to search for in syslog messages. The script will monitor for any of these.

**Example:**

```bash
./nightly-syslog-whisperer.sh ERROR WARNING CRITICAL
```

This will continuously monitor `/var/log/syslog` (or equivalent) for lines containing "ERROR", "WARNING", or "CRITICAL" and print them with a touch of flair.

## How it Works

The script uses `tail -f` to follow the syslog file in real-time. It pipes the output through `grep` to filter for the specified keywords. Each matching line is then processed to add a whimsical prefix, making potentially alarming messages feel a bit more like cryptic pronouncements.

## Installation

1.  Save the script as `nightly-syslog-whisperer.sh`.
2.  Make it executable: `chmod +x nightly-syslog-whisperer.sh`.

## Testing

Run the provided test script:

```bash
./tests/run_tests.sh
```
