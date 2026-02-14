# nightly-ghostly-file-purifier

**Nightly Ghostly File Purifier** – a playful Bash utility that scans a directory for files larger than a given size threshold. It can either list those files or compress them into ``.gz`` archives, turning bulky data into ethereal ghosts.

## Features

- Recursively search any directory for files exceeding a size limit (in megabytes).
- Optionally compress each oversized file with ``gzip`` while keeping the original (so you can verify the transformation).
- Friendly, color‑less output suitable for scripts, CI pipelines, or a midnight terminal session.

## Installation

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/main.sh
```

The utility has **no external dependencies** beyond standard Unix tools (`find`, `gzip`, `dd`). It works with Bash 4+.

## Usage

```bash
./src/main.sh -d /path/to/scan -s SIZE_MB [-c]
```

- ``-d`` – Directory to scan (required).
- ``-s`` – Size threshold in megabytes (required).
- ``-c`` – Compress the found files. If omitted, the script only lists them.

### Examples

List files larger than 100 MiB in ``/var/log``:

```bash
./src/main.sh -d /var/log -s 100
```

Compress files larger than 50 MiB in the current directory:

```bash
./src/main.sh -c -d . -s 50
```

## Exit Codes

- ``0`` – Successful execution (whether files were found or not).
- ``1`` – Invalid arguments or runtime error.

## Testing

Run the bundled test suite:

```bash
./tests/test_main.sh
```

The tests create temporary files, verify detection, and ensure compression works without touching your real data.
