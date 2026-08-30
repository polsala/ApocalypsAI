# nightly-ghostbuster

Detects zombie (defunct) processes and optionally kills their parent processes.

## Usage

```sh
./src/ghostbuster.sh [--dry-run]
```

- `--dry-run` : only list zombies without killing.

## How it works

The script uses `ps` to find processes with state `Z` (zombie). For each zombie, it attempts to kill its parent process (unless the parent is PID 1).

## Safety

Killing parent processes can affect running services. Use `--dry-run` first.

## Tests

Run the test suite:

```sh
cd tests && ./test_ghostbuster.sh
```
