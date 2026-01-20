# nightly-void-whistle

A blazingly fast CLI utility written in Rust to detect silent failures (i.e., missing expected log lines) in log streams.

## Usage

```bash
void-whistle --pattern "ERROR" --input logs.txt
```

## Options

- `--pattern <PATTERN>`: The log line pattern to watch for (required).
- `--input <FILE>`: Input log file (optional; defaults to stdin).
- `--invert`: Flag to alert when pattern ISN’T found (i.e., silent failure).

## Example

```bash
echo -e "INFO start\nINFO end" | void-whistle --pattern "ERROR" --invert
```

This will alert because no `ERROR` line was found.
