Nightly Echo Echo
=================

A whimsical Bash utility that prints a random phrase from a curated list of whimsical sayings.
Use `./echo_echo.sh` to get a random phrase, or `./echo_echo.sh --list` to see all available phrases.

Usage
-----

```bash
./echo_echo.sh          # prints a random phrase
./echo_echo.sh --list   # lists all phrases
```

The script uses Bash's `$RANDOM` variable for randomness.
For deterministic output in tests, set the `RANDOM` environment variable before invoking the script.
