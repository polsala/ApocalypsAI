# nightly-bash-apocalypse-disk-alert

## Overview

`nightly-bash-apocalypse-disk-alert` is a tiny Bash script that checks the system's disk usage (via `df -h`). If any mounted filesystem is using **80%** or more of its capacity, the script prints a randomly selected apocalypse‑themed warning phrase.  Otherwise it reports that *all is calm*.

The utility is deliberately whimsical – perfect for adding a bit of drama to cron‑job logs, CI pipelines, or just for fun during system admin sessions.

## Features

- Parses `df -h` output safely.
- Threshold is configurable via the `THRESHOLD` variable (default **80**).
- Uses a static list of ten dramatic phrases.
- Deterministic phrase selection when the `RANDOM` variable is set (useful for testing).

## Installation

```bash
# Clone the repository (or copy the folder) and make the script executable
cd bash-utils/nightly-bash-apocalypse-disk-alert/src
chmod +x main.sh
```

You can also symlink it to a directory in your `$PATH` for easy access.

## Usage

```bash
./main.sh
```

Typical output when a partition is over the threshold:

```
The seas rise!
```

When everything is under the limit:

```
All clear. No apocalypse imminent.
```

## Testing

The utility ships with a deterministic Bash test that mocks `df` output and forces a known `RANDOM` value.

```bash
cd tests
bash test_main.sh
```

The test should print `Test passed.` if everything works.

## Customisation

- **Change the threshold**: edit the `THRESHOLD` variable in `src/main.sh`.
- **Add your own phrases**: modify the `APOC_PHRASES` array.

Enjoy the drama!
