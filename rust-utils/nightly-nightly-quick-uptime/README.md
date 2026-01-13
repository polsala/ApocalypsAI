Nightly Quick Uptime
====================

A whimsical Rust CLI that reports system uptime in poetic prose.

Installation
------------

```bash
cargo install nightly-quick-uptime
```

Usage
-----

```bash
nightly-quick-uptime
```

Output

````
The system has been awake for 0 days, 3 hours, 25 minutes, and 45 seconds. Keep calm and carry on!
```

The utility reads `/proc/uptime` by default, but you can point it to a custom file via the `UPTIME_FILE` environment variable for testing or custom data.
