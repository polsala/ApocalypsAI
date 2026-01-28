# nightly-apt-cleanup-helper

Utility to preview and optionally clean up unnecessary APT packages on Debian/Ubuntu systems.

## Features

- **Dry‑run mode** (`--dry-run`) lists packages that would be removed by `apt-get autoremove`.
- **Clean mode** (`--clean`) actually runs `apt-get autoremove -y` and `apt-get clean`.
- Safe for CI: when the environment variable `APT_MOCK=1` is set, the script simulates `apt-get` output for testing.

## Usage

```sh
./src/main.sh --dry-run   # Show packages that would be removed
./src/main.sh --clean     # Actually remove and clean
```

## How it works

The script wraps `apt-get -s autoremove` (simulation) and parses the output to extract package names. In mock mode it prints a fixed example output.

## Testing

Run the bundled test script:

```sh
bash tests/test_main.sh
```
