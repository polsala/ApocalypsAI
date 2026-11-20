# nightly-wasteland-dustbuster

**What it does**

`dustbuster` scans a directory (default: `/var/log`) for files older than a configurable number of days and compresses them with `gzip`.  It includes a *dry‑run* flag so you can see what would happen before any files are touched.

---

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-wasteland-dustbuster

# Make the script executable
chmod +x src/dustbuster.sh
```

## Usage

```bash
./src/dustbuster.sh [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-p <path>` | Directory to scan. Default: `/var/log`. |
| `-d <days>` | Minimum age of files (in days) to target. Default: `7`. |
| `-n` | **Dry‑run** – only show which files would be compressed, do not modify anything. |
| `-h` | Show help message. |

### Examples

*Compress logs older than 10 days in `/var/log`*:
```bash
./src/dustbuster.sh -d 10
```

*Preview what would happen in a custom directory*:
```bash
./src/dustbuster.sh -p /tmp/mylogs -d 5 -n
```

---

## Testing

Run the bundled test suite with:
```bash
bash tests/test_dustbuster.sh
```
All tests should pass on any Unix‑like system with Bash and `gzip` installed.

---

## License

MIT – see the root `LICENSE` file.
