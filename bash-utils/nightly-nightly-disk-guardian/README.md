# nightly-disk-guardian

Utility monitors root filesystem disk usage. If usage exceeds a configurable threshold (default **80%**), it prints a random apocalypse‑themed warning.

## Usage

```sh
./src/main.sh [threshold]
```

* `threshold` – optional integer percent (0‑100). If omitted, **80** is used.

### Example

```sh
# Warn when usage goes above 75%
./src/main.sh 75
```

## How it works

1. Runs `df -h /` (or uses the `MOCK_DF` env var for testing) to obtain the usage percent.
2. If the usage is greater than the supplied threshold, a random message from a built‑in list is displayed. The messages embed the current usage percentage.
3. Otherwise a calm confirmation is printed.

## Testing

The test suite runs offline by feeding a mock `df` output via the `MOCK_DF` environment variable.

```sh
bash tests/test_main.sh
```

All tests should pass on any POSIX‑compatible system with Bash.
