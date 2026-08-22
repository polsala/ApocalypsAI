# nightly-quick-disk-usage-report

Utility that scans a directory and prints a concise disk usage summary in both human‑readable and JSON formats. Useful for CI pipelines or quick local checks.

## Usage

```sh
./src/disk_report.sh <path> [threshold_bytes]
```

- `<path>`: directory to analyze (default: current directory)
- `threshold_bytes` (optional): only report if size exceeds this value; otherwise exits with code 0 and no output.

## Output

- Human‑readable line: `Size: 1.23 MiB (1290240 bytes)`
- JSON line: `{"path":"...","size_bytes":1290240,"size_human":"1.23 MiB"}`

## Exit codes

- `0` – success (or size below threshold)
- `1` – error (invalid path)
